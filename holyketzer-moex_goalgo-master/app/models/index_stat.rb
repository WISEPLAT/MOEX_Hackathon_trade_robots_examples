class IndexStat
  # mr - monthly return
  # yr - yearly return
  # md - monthly drawdown
  # yd - yearly drawdown
  # rsd - relative standard deviation
  attr_reader :avg_mr, :avg_yr, :max_md, :max_yd, :rsd, :sharp

  class << self
    def calc(price_line)
      # Relative standard deviation
      prices = Daru::Vector.new(price_line.map { |row| row[2] }) # close prices
      std = prices.std
      rsd = 100 * std / prices.mean

      min_date = price_line.first[0]
      max_date = price_line.last[0]
      first_price = price_line.first[2]
      last_price = price_line.last[2]

      # Monthly return
      monthes = (max_date.to_time - min_date.to_time) / 1.month
      avg_mr = 100 * (last_price / first_price) ** (1 / monthes) - 100

      # Yearly return
      years = (max_date.to_time - min_date.to_time) / 1.year
      avg_yr = 100 * (last_price / first_price) ** (1 / years) - 100

      # Monthly drawdown
      max_md = calculate_drawdown(price_line, :month)
      max_yd = calculate_drawdown(price_line, :year)

      # Sharpe ratio
      sharp = 0 # avg_yr / std TBD

      new(avg_mr.to_f, avg_yr.to_f, max_md.to_f, max_yd.to_f, rsd.to_f, sharp.to_f)
    end

    def calculate_drawdown(data, period = :month)
      # Step 1: Transform the array into a hash
      data_by_period = Hash.new { |hash, key| hash[key] = [] }
      data.each { |date, _, close| data_by_period[date.send(period)] << close }

      max_drawdown = 0.0

      # Step 2: Calculate maximum drawdown for each period
      data_by_period.each do |period, values|
        peak_value = values.first
        drawdown = 0.0

        values.each do |value|
          drawdown = [drawdown, (value - peak_value) / peak_value].min
          peak_value = [peak_value, value].max
        end

        # Step 3: Find the maximum drawdown among all periods
        max_drawdown = [max_drawdown, drawdown].min
      end

      100 * max_drawdown
    end
  end

  private

  def initialize(avg_mr, avg_yr, max_md, max_yd, rsd, sharp)
    @avg_mr = avg_mr
    @avg_yr = avg_yr
    @max_md = max_md
    @max_yd = max_yd
    @rsd = rsd
    @sharp = sharp
  end
end
