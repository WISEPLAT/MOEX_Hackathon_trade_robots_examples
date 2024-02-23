class IndexCalculator
  REVIEW_PERIOD = "review_period".freeze
  REVIEW_PERIOD_Q = "quarterly".freeze
  REVIEW_PERIOD_Y = "yearly".freeze

  FILTERS = "filters".freeze
  FILTERS_LL = "listing_level".freeze
  FILTERS_SECTOR = "sector".freeze
  FILTERS_TICKERS = "tickers".freeze

  SELECTION = "selection".freeze
  SELECTION_MARKET_CAP = "market_cap".freeze
  SELECTION_MOMENTUM = "momentum".freeze
  SELECTION_TOP = "top".freeze
  SELECTION_PERIOD = "period".freeze
  SELECTION_BENCHMARK = "benchmark".freeze

  MOMENTUM_DROP_HIGH_BETA = 0.1
  MOMENTUM_PICK_HIGH_RETURN = 0.5
  MOMENTUM_MIN_DAYS = 100

  WEIGHING = "weighing".freeze
  WEIGHING_EQUAL = "equal".freeze
  WEIGHING_MARKET_CAP = "market_cap".freeze

  INDEX_START_POINT = 1_000
  INDEX_START_MONEY = 1_000_000_000

  THRESHOLD_SHARES_LOAD_PREV_PRICE = 2

  class ShareCoeffs
    attr_reader :share_id, :beta, :returns

    def initialize(share_id:, beta:, returns:)
      @share_id = share_id
      @beta = beta
      @returns = returns
    end
  end

  class DelistedShare
    attr_reader :share_id, :listed_till, :last_close

    def initialize(share_id:, listed_till:, last_close:)
      @share_id = share_id
      @listed_till = listed_till
      @last_close = last_close
    end
  end

  class << self
    def build_index(custom_index)
      custom_index.update!(status: "in_progress", progress: 0)
      CustomIndexItem.where(custom_index: custom_index).delete_all
      CustomIndexPrice.where(custom_index: custom_index).delete_all
      delisted_shares = load_delisted_shares

      settings = custom_index.settings
      prev_index_items = []
      index_items_per_period = date_iterator(settings[REVIEW_PERIOD]) do |date, end_date|
        share_caps = filter_shares(date, end_date, settings[FILTERS])
        share_caps = select_shares(share_caps, date, settings[SELECTION])
        share_cap_by_weight = weigh_shares(share_caps, settings[WEIGHING])
        index_items = create_index_items(custom_index, date, share_cap_by_weight, prev_index_items)

        puts "#{date} #{share_caps.size} shares #{share_caps.map(&:secid).join(", ")}"
        prev_index_items = index_items
      end.reject(&:empty?)

      last_date = nil
      total_count = index_items_per_period.size
      i = 0
      index_items_per_period.each_cons(2) do |prev_index_items, index_items|
        from_date = prev_index_items.first.date
        to_date = index_items.first.date - 1.day
        create_index_prices(custom_index, from_date, to_date, prev_index_items, delisted_shares)
        last_date = to_date
        i += 1
        custom_index.update!(progress: (i * 100 / total_count))
      end

      if last_date
        create_index_prices(custom_index, last_date, Date.today, index_items_per_period[-1], delisted_shares)
      end

      price_line = CustomIndexPrice.where(custom_index: custom_index)
        .order(date: :asc)
        .pluck(:date, :open, :close)
      index_stat = IndexStat.calc(price_line)
      custom_index.update!(
        status: "done", progress: 100, error: nil,
        avg_mr: index_stat.avg_mr,
        avg_yr: index_stat.avg_yr,
        max_md: index_stat.max_md,
        max_yd: index_stat.max_yd,
        rsd: index_stat.rsd,
        sharp: index_stat.sharp,
      )
    end

    def filter_shares(date, end_date, filters)
      share_caps = ShareCap.where(date: date)

      filters.each do |filter_key, filter_value|
        case filter_key
        when FILTERS_LL
          share_caps = share_caps.where(share_id: Share.where(list_level: filter_value).select(:id))
        when FILTERS_TICKERS
          share_caps = share_caps.where(secid: filter_value)
        when FILTERS_SECTOR
          share_caps = share_caps.where(share_id: Share.where(share_sector_id: filter_value).select(:id))
        else
          raise "Unknown filter #{filter}"
        end
      end

      # filter by count of traded days
      # about 70% of working days per year, consider 50% of days ok
      before_date = date - (end_date - date)
      traded_days_threshold = ((end_date - date) * 0.5).to_i
      liquid_share_ids = SharePrice.where(share_id: share_caps.select(:share_id))
        .where("date <= ?", date)
        .where("date >= ?", before_date)
        .where("close > 0")
        .group(:share_id)
        .having("count(*) >= ?", traded_days_threshold)
        .pluck(:share_id)

      share_caps = share_caps.where(share_id: liquid_share_ids)
      share_caps
    end

    private

    def select_shares(share_caps, date, selection)
      selection_key, selection_value = *selection
      case selection_key
      when SELECTION_MARKET_CAP
        share_caps = share_caps.order(cap: :desc).limit(selection_value[SELECTION_TOP])
      when SELECTION_MOMENTUM
        share_ids = select_with_momentum(share_caps, date, selection_value[SELECTION_PERIOD], selection_value[SELECTION_BENCHMARK])
        share_caps = share_caps.where(share_id: share_ids)#.limit(selection_value[SELECTION_TOP])
      else
        raise "Unknown selection #{selection}"
      end
    end

    # https://at6.livejournal.com/29233.html
    # https://alphaarchitect.com/2015/12/quantitative-momentum-investing-philosophy/
    def select_with_momentum(share_caps, date, period_days, benchmark_index)
      shares_index = SharesIndex.where(secid: benchmark_index).first
      index_prices_by_date = IndexPrice.where(shares_index: shares_index)
        .where("date <= ?", date)
        .where("date >= ?", date - period_days.days)
        .where("close > 0")
        .order(date: :asc)
        .pluck(:date, :close)

      share_coeffs = share_caps.map do |share_cap|
        share_prices_by_date = SharePrice.where(share: share_cap.share)
          .where("date <= ?", date)
          .where("date >= ?", date - period_days.days)
          .where("close > 0")
          .order(date: :asc)
          .pluck(:date, :close)

        index_prices, share_prices = *allign_prices(index_prices_by_date, share_prices_by_date)
        index_vector = Daru::Vector.new(relative_growth(index_prices))
        share_vector = Daru::Vector.new(relative_growth(share_prices))

        if index_vector.size > MOMENTUM_MIN_DAYS
          ShareCoeffs.new(
            share_id: share_cap.share_id,
            beta: (share_vector.covariance_population(index_vector) / index_vector.variance_population).to_f,
            returns: ((share_prices.last - share_prices.first) / share_prices.first).to_f,
          )
        else
          nil
        end
      end

      share_coeffs = share_coeffs.compact
      share_coeffs = share_coeffs.sort_by(&:beta).take((share_coeffs.size*(1-MOMENTUM_DROP_HIGH_BETA)).to_i)
      share_coeffs = share_coeffs.sort_by(&:returns).take((share_coeffs.size*MOMENTUM_PICK_HIGH_RETURN).to_i)
      share_coeffs.map(&:share_id)
    end

    def allign_prices(index_prices, share_prices)
      index_vector = []
      share_vector = []

      share_prices = share_prices.to_h
      index_prices.each do |index_date, index_price|
        if (share_price = share_prices[index_date])
          index_vector << index_price
          share_vector << share_price
        end
      end

      [index_vector, share_vector]
    end

    def relative_growth(prices)
      res = []
      prices.each_cons(2) do |prev_price, price|
        res << (price - prev_price) / prev_price.to_f
      end
      res
    end

    def weigh_shares(share_caps, weighing)
      case weighing
      when WEIGHING_EQUAL
        share_caps.map { |share_cap| [share_cap, 1.0 / share_caps.size] }.to_h
      when WEIGHING_MARKET_CAP
        total_cap = share_caps.sum { |x| BigDecimal(x.cap) }
        share_caps.map { |share_cap| [share_cap, share_cap.cap / total_cap] }.to_h
      else
        raise "Unknown weighing `#{weighing}`"
      end
    end

    def create_index_items(custom_index, date, share_cap_by_weight, prev_index_items)
      if share_cap_by_weight.size == 0
        return []
      end

      share_ids = share_cap_by_weight.keys.map(&:share_id) + prev_index_items.map(&:share_id)
      prices_by_share_id = load_last_prices(share_ids, date)

      if prev_index_items.size > 0
        total_money = prev_index_items.sum { |item| item.shares_count * prices_by_share_id[item.share_id].close }
      else
        total_money = INDEX_START_MONEY
        custom_index.update!(coeff_d: total_money / INDEX_START_POINT)
      end

      CustomIndexItem.transaction do
        CustomIndexItem.where(custom_index: custom_index, date: date).delete_all

        share_cap_by_weight.map do |share_cap, weight|
          shares_count = (total_money * weight / prices_by_share_id[share_cap.share_id].close)

          CustomIndexItem.create!(
            custom_index: custom_index,
            share: share_cap.share,
            date: date,
            shares_count: shares_count,
            weight: weight,
          )
        end
      end
    end

    def create_index_prices(custom_index, from_date, to_date, index_items, delisted_shares_data)
      CustomIndexPrice.transaction do
        CustomIndexPrice.where(custom_index: custom_index)
          .where("date >= ?", from_date)
          .where("date <= ?", to_date)
          .delete_all

        attrs = []

        (from_date..to_date).each do |date|
          share_ids = index_items.map(&:share_id)
          prices_by_share_id = {}

          required_shares = {}
          delisted_shares = {}
          share_ids.each do |share_id|
            if delisted_shares_data[share_id] && delisted_shares_data[share_id].listed_till < date
              delisted_shares[share_id] = true
            else
              required_shares[share_id] = true
            end
          end

          SharePrice.where(share_id: share_ids, date: date).where("open > 0 and close > 0").each do |share_price|
            prices_by_share_id[share_price.share_id] = share_price
            required_shares.delete(share_price.share_id)
          end

          if required_shares.any? && required_shares.size <= THRESHOLD_SHARES_LOAD_PREV_PRICE
            load_last_prices(required_shares.keys, date).each do |share_id, share_price|
              prices_by_share_id[share_id] = share_price
              required_shares.delete(share_id)
            end
          end

          if prices_by_share_id.size > 0 && required_shares.size == 0
            attrs << {
              custom_index_id: custom_index.id,
              date: date,
              open: calc_index_points(date, index_items, prices_by_share_id, custom_index, :open, delisted_shares_data),
              close: calc_index_points(date, index_items, prices_by_share_id, custom_index, :close, delisted_shares_data),
              # low: calc_index_points(index_items, prices_by_share_id, custom_index, :low), # should be composed from smaller periods
              # high: calc_index_points(index_items, prices_by_share_id, custom_index, :high),
              # volume: 0, # not sure how to calculate it
            }
          elsif prices_by_share_id.size > 0
            # Consider if prices_by_share_id.size == 0 then it's a weekend or holiday
            puts "Not all prices for #{date} missed: #{required_shares.keys.join(', ')}"
          end
        end

        CustomIndexPrice.insert_all(attrs)
      end
    end

    def calc_index_points(date, index_items, prices_by_share_id, custom_index, price_attr, delisted_shares_data)
      total = index_items.sum do |index_item|
        if delisted_shares_data[index_item.share_id] && date > delisted_shares_data[index_item.share_id].listed_till
          index_item.shares_count * delisted_shares_data[index_item.share_id].last_close # keep as cash in index until next quarter/year
        else
          index_item.shares_count * prices_by_share_id[index_item.share_id].send(price_attr)
        end
      end
      total / custom_index.coeff_d
    end

    def load_last_prices(share_ids, date)
      SharePrice.joins(
        <<~SQL
          JOIN (
            SELECT share_id, MAX(date) AS max_date
            FROM share_prices
            WHERE date <= '#{date}' and share_id in (#{share_ids.join(", ")}) and close > 0
            GROUP BY share_id
          ) mdp ON share_prices.share_id = mdp.share_id AND share_prices.date = mdp.max_date
        SQL
      ).map do |price|
        # Fail fast in case of too old price
        if date - price.date > 7.days
          raise "Too price for #{price.share.secid} on #{date}"
        end
        [price.share_id, price]
      end.to_h
    end

    def load_delisted_shares
      listed_till_by_share_id = Share.where.not(listed_till: nil).pluck(:id, :listed_till).to_h
      last_prices = load_last_prices(listed_till_by_share_id.keys, Date.today)

      listed_till_by_share_id.map do |share_id, listed_till|
        [
          share_id,
          DelistedShare.new(
            share_id: share_id,
            listed_till: listed_till,
            last_close: last_prices[share_id]&.close,
          )
        ]
      end.to_h
    end

    def date_iterator(period)
      start = SharePrice.minimum("date")
      case period
      when REVIEW_PERIOD_Q
        start = start.end_of_quarter
        step = 3.months
        method = "end_of_quarter"
      when REVIEW_PERIOD_Y
        start = start.end_of_year
        step = 1.year
        method = "end_of_year"
      else
        raise "Unknown period #{period}"
      end

      res = []
      while start < Date.today
        start = start.send(method)
        res << (yield start, (start + step).send(method))
        start += step
      end
      res
    end
  end
end
