class ShareSplitsService
  class << self
    def fix_data
      # Date, SECID, before, after
      [

        ["2014-12-30", "IRAO", 100, 1],
        ["2016-04-27", "RGSS", 1, 15],
        ["2023-01-18", "ROLO", 1, 10],
      ].each do |date, secid, before, after|
        share = Share.find_by(secid: secid)

        if !ShareSplit.find_by(date: date, share: share)
          Share.transaction do
            ShareSplit.create!(
              date: date,
              share: share,
              before: before,
              after: after
            )

            coeff = before.to_f / after

            SharePrice.where(share_id: share.id)
              .where("date < ?", date)
              .update_all(
                <<~SQL
                  close = close * #{coeff},
                  open = open * #{coeff},
                  low = low * #{coeff},
                  high = high * #{coeff},
                  waprice = waprice * #{coeff}
                SQL
              )
          end
        end
      end
    end

    def find_splits
      SharePrice.pluck("distinct(share_id)").each do |share_id|
        query = <<~SQL
          WITH RankedData AS (
            SELECT
              share_id,
              date,
              close,
              LAG(close) OVER (ORDER BY date) AS prev_close,
              LEAD(close) OVER (ORDER BY date) AS next_close
            FROM
              share_prices
              where share_id = #{share_id} and close > 0
          )
          SELECT
            share_id,
            date,
            prev_close,
            close,
            next_close
          FROM (
            SELECT
              share_id,
              date,
              close,
              LAG(date) OVER (ORDER BY date) AS prev_date,
              prev_close,
              LEAD(date) OVER (ORDER BY date) AS next_date,
              next_close
            FROM RankedData
          ) AS Subquery
          WHERE ABS(close - prev_close) > 2 * close OR ABS(close - next_close) > 2 * close;
        SQL

        SharePrice.connection.execute(query).each do |row|
          secid = Share.find(share_id).secid

          if secid == "PRFN" || # issue with data 4 years gap
            secid == "POGR" # delisted on low close
            next
          end
          puts row.to_h.merge("secid" => secid)
          raise "Stop! Found split!"
        end
      end
    end
  end
end
