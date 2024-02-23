class AlgopackLoader
  include Singleton

  START_DATE = Date.parse("1997-03-24")

  def load_shares(skip_existing: false)
    # Fetch all pages of shares with pagination
    loaded_secids = Share.pluck(:secid).to_set

    offset = 0
    begin
      shares = AlgopackFetcher.instance.fetch_shares(offset: offset, limit: 100)

      shares.each do |share|
        # Save the share information to the DB using the Security model
        if skip_existing && loaded_secids.include?(share["secid"])
          next
        end

        if !Share::SHARE_TYPES.include?(share["type"])
          next
        end

        # Fetch information of the particular share
        share_info = AlgopackFetcher.instance.fetch_share(share["secid"])

        attrs = {
          secid: share_info["secid"],
          name: share_info["name"],
          short_name: share_info["shortname"],
          isin: share_info["isin"] || Share::NO_ISIN,
          issue_size: share_info["issuesize"].to_i,
          nominal_price: Money.from_amount(share_info["facevalue"], share_info["faceunit"]),
          issue_date: share_info["issuedate"],
          history_from: share_info["history_from"],
          list_level: share_info["listlevel"].to_i,
          sec_type: share_info["type"],
        }
        if (share = Share.find_by(secid: share_info["secid"]))
          share.update!(attrs)
        else
          share = Share.new(attrs)
          share.save!
        end
      end
      offset += shares.size
    end while shares.size > 0
  end

  def load_cap
    caps = AlgopackFetcher.instance.fetch_shares_cap

    caps.compact.each do |secid, cap|
      if (share = Share.find_by(secid: secid))
        share.update!(cap: cap)
      end
    end
  end

  def load_shares_count
    version = 1
    shares = Share.where("version < ?", version)

    shares.each do |share|
      if (counts = SmartlabListedSharesFetcher.instance.fetch_for(share.secid))
        counts.each do |date, count|
          if count != nil
            ShareMacroStat.create!(
              share: share,
              secid: share.secid,
              date: date,
              shares_count: count,
            )
          end
        end
      end
      share.update!(version: version)
    end
  end

  def load_all_history_prices
    secids = ShareMacroStat.pluck("distinct(secid)")
    secids.each do |secid|
      label = "#{secid} (#{secids.index(secid)+1}/#{secids.size})"
      puts "Loading history prices for #{label}"
      share = Share.find_by(secid: secid)
      from = SharePrice.where(secid: secid).order(date: :desc).first&.date
      if from
        from += 1.day
      else
        from = START_DATE
      end

      prev_from = from - 1.day
      while from < Date.today && prev_from != from
        puts "Loading history prices for #{label} from #{from}"
        prev_from = from

        prices = AlgopackFetcher.instance.fetch_history_prices(secid, from: from, to: Date.today)

        attrs = prices.map do |price|
          date = Date.parse(price["tradedate"])
          from = date + 1.day

          {
            share_id: share.id,
            secid: secid,
            date: date,
            open: price["open"],
            close: price["close"],
            low: price["low"],
            high: price["high"],
            volume: price["volume"].to_i,
            waprice: price["waprice"],
          }
        end

        SharePrice.insert_all(attrs)
      end
    end
  end

  def load_indexes
    indexes = AlgopackFetcher.instance.fetch_indexes(["IMOEX", "RTSI"])
    indexes.each do |index|
      attrs = {
        secid: index["secid"],
        name: index["name"],
        short_name: index["shortname"],
        currency: index["currencyid"],
      }

      if (shares_index = SharesIndex.find_by(secid: index["secid"]))
        shares_index.update!(**attrs)
      else
        SharesIndex.create!(**attrs)
      end
    end
  end

  def load_all_index_history_prices
    shares_indexes = SharesIndex.all
    shares_indexes.each_with_index do |shares_index, i|
      label = "#{shares_index.secid} (#{i+1}/#{shares_indexes.size})"
      puts "Loading history prices for #{label}"
      from = IndexPrice.where(secid: shares_index.secid).order(date: :desc).first&.date
      if from
        from += 1.day
      else
        from = START_DATE
      end

      prev_from = from - 1.day
      while from < Date.today && prev_from != from
        puts "Loading history prices for #{label} from #{from}"
        prev_from = from

        prices = AlgopackFetcher.instance.fetch_indexes_history(shares_index.secid, from: from, to: Date.today)

        attrs = prices.map do |price|
          date = Date.parse(price["tradedate"])
          from = date + 1.day

          {
            shares_index_id: shares_index.id,
            secid: shares_index.secid,
            date: date,
            open: price["open"],
            close: price["close"],
            low: price["low"],
            high: price["high"],
            volume: price["volume"].to_i,
          }
        end

        IndexPrice.insert_all(attrs)
      end
    end
  end

  def load_currencies
    currencies = AlgopackFetcher.instance.fetch_currencies
    currencies.each do |currency|
      attrs = {
        secid: currency["secid"],
        name: currency["secname"],
        short_name: currency["shortname"],
        currency: currency["currencyid"],
        lot_size: currency["lotsize"],
        minstep: currency["minstep"],
        status: currency["status"],
        remarks: currency["remarks"],
        face: Money.from_amount(currency["facevalue"], currency["faceunit"]),
      }

      if (currency = Currency.find_by(secid: currency["secid"]))
        currency.update!(**attrs)
      else
        Currency.create!(**attrs)
      end
    end
  end

  def load_all_currency_history_prices
    currencies = Currency.all
    currencies.each_with_index do |currency, i|
      label = "#{currency.secid} (#{i+1}/#{currencies.size})"
      puts "Loading history prices for #{label}"
      from = CurrencyPrice.where(secid: currency.secid).order(date: :desc).first&.date
      if from
        from += 1.day
      else
        from = START_DATE
      end

      prev_from = from - 1.day
      while from < Date.today && prev_from != from
        puts "Loading history prices for #{label} from #{from}"
        prev_from = from

        prices = AlgopackFetcher.instance.fetch_currencies_history(currency.secid, from: from, to: Date.today)

        attrs = prices.map do |price|
          date = Date.parse(price["tradedate"])
          from = date + 1.day

          {
            currency_id: currency.id,
            secid: currency.secid,
            date: date,
            open: nil_if_zero(price["open"]),
            close: nil_if_zero(price["close"]),
            low: nil_if_zero(price["low"]),
            high: nil_if_zero(price["high"]),
            waprice: nil_if_zero(price["waprice"]),
          }
        end

        CurrencyPrice.insert_all(attrs)
      end
    end
  end

  def load_listed_till
    total = Share.count
    found = 0
    Share.all.each_with_index do |share, i|
      puts "#{i+1}/#{total} #{share.secid}"
      listed_till = AlgopackFetcher.instance.fetch_listed_till(share.secid)
      share.update!(listed_till: listed_till)

      if listed_till
        found += 1
      end
    end
    puts "Found listed till for #{found}/#{total} shares"
  end

  private

  def nil_if_zero(value)
    value == 0 ? nil : value
  end
end
