class CapCalculator
  class << self
    def calc
      ShareMacroStat.find_each do |share_macro_stat|
        share_price = SharePrice.where(share_id: share_macro_stat.share_id)
          .where("date <= ?", share_macro_stat.date)
          .where("waprice > 0")
          .order(date: :desc)
          .limit(1)
          .first

        if share_price
          diff = share_macro_stat.date - share_price.date
          puts "#{share_price.secid} #{share_macro_stat.date} diff: #{diff}"
          if diff > 7.days
            raise "diff > 7.days"
          end

          share_cap = calculate_share_cap(share_macro_stat.shares_count, share_price)
          share_macro_stat.update(cap: share_cap)
        else
          puts "No share price for #{share_macro_stat.secid} #{share_macro_stat.date}"
        end
      end
    end

    def fill_share_caps
      ShareMacroStat.pluck("distinct(secid)").each do |secid|
        prev_share_macro_stat = ShareMacroStat.where(secid: secid).order(date: :asc).first
        date = prev_share_macro_stat.date

        while date < Date.today
          share_macro_stat = ShareMacroStat.where(secid: secid, date: date).first
          shares_count = share_macro_stat&.shares_count || prev_share_macro_stat.shares_count

          share_price = SharePrice.where(secid: secid)
            .where("date <= ?", date)
            .where("waprice > 0")
            .order(date: :desc)
            .limit(1)
            .first

          if share_price
            diff = date - share_price.date
            puts "#{secid} #{date} diff: #{diff}"
            if diff > 7.days
              raise "diff > 7.days"
            end

            cap = calculate_share_cap(shares_count, share_price)
            ShareCap.find_or_create_by!(share_id: prev_share_macro_stat.share_id, date: date) do |share_cap|
              share_cap.cap = cap
              share_cap.secid = secid
            end
          else
            puts "No share price for #{secid} #{date}"
          end

          if share_macro_stat
            prev_share_macro_stat = share_macro_stat
          end
          date = (date + 3.months).end_of_quarter
        end
      end
    end

    private

    def calculate_share_cap(shares_count, share_price)
      shares_count * share_price.waprice
    rescue StandardError => e
      p share_price
      raise e
    end
  end
end
