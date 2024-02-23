
class CustomIndexesController < ApplicationController
  before_action :authenticate_user!

  skip_before_action :verify_authenticity_token, only: [:filter_check]

  def index
    @custom_indexes = custom_indexes_scope.order(avg_yr: :desc, rsd: :asc)
    if @custom_indexes.any?
      prices = @custom_indexes.map do |custom_index|
        prices = CustomIndexPrice.where(custom_index_id: custom_index.id).order(date: :asc).pluck(:date, :open, :close)
        [custom_index.name, prices]
      end.to_h

      @benchmark, @price_lines = *normalize_prices!(prices)
      @bm_stat = IndexStat.calc(@benchmark)
    end
  end

  def show
    @custom_index = custom_indexes_scope.find(params[:id])
    @custom_index_items = CustomIndexItem.preload(:share)
      .where(custom_index_id: @custom_index.id)
      .order(date: :desc)
      .to_a
      .group_by(&:date)
    @custom_index_prices = CustomIndexPrice.where(custom_index_id: @custom_index.id).order(date: :asc).pluck(:date, :open, :close)

    if @custom_index_prices.any?
      @benchmark, @price_lines = *normalize_prices!(@custom_index.name => @custom_index_prices)
      @bm_stat = IndexStat.calc(@benchmark)
    end
  end

  def new
    date = ShareCap.order(date: :desc).first&.date
    @shares_count = date ? ShareCap.where(date: date).count : 0

    @shares = Share.order(:short_name).pluck(:secid, :short_name)
    @sectors = ShareSector.order(:name).pluck(:id, :name)
    @custom_index = CustomIndex.new
  end

  def filter_check
    listing_levels = params[:listing]&.map(&:to_i)
    sectors = params[:sectors]&.map(&:to_i)
    secids = params[:tickers]

    if (date = ShareCap.order(date: :desc).first&.date)
      filters = {
        IndexCalculator::FILTERS_LL => listing_levels,
        IndexCalculator::FILTERS_SECTOR => sectors,
        IndexCalculator::FILTERS_TICKERS => secids,
      }.compact

      count = IndexCalculator.filter_shares(date, date + 3.months, filters).size
      render json: { count: count }
    else
      render json: { error: 'No data available' }
    end
  end

  def create
    @custom_index = CustomIndex.new(custom_index_params)
    # If we index with the same name already exists
    if !@custom_index.save && @custom_index.errors.first&.attribute == :name
      @custom_index.name += " #{SecureRandom.hex(1)}" # make name unique and don't bother user with it
    end

    if @custom_index.save
      BuildIndexJob.perform_async(@custom_index.id)
      redirect_to custom_index_path(@custom_index)
    else
      render :new
    end
  end

  def destroy
    @custom_index = custom_indexes_scope.find(params[:id])

    CustomIndex.transaction do
      CustomIndexPrice.where(custom_index_id: @custom_index.id).delete_all
      CustomIndexItem.where(custom_index_id: @custom_index.id).delete_all
      @custom_index.destroy
    end

    redirect_to custom_indexes_path, notice: "#{@custom_index.name} удалён"
  end

  private

  def custom_indexes_scope
    CustomIndex.where(user: current_user)
  end

  def normalize_prices!(price_lines)
    index = SharesIndex.find_by(secid: "IMOEX")
    min_date = price_lines.values.reject(&:blank?).map { |line| line[0][0] }.min
    max_date = price_lines.values.reject(&:blank?).map { |line| line[-1][0] }.max

    benchmark = IndexPrice.where(shares_index: index)
      .where("date >= ?", min_date)
      .where("date <= ?", max_date)
      .order(date: :asc)
      .pluck(:date, :open, :close)

    benchmark_by_date = benchmark.to_h { |row| [row[0], row[-1]] }
    res = []

    price_lines.each do |name, price_line|
      if price_line.any?
        mapped_price_line = []
        coeff = nil

        price_line.each do |date, open, close|
          if coeff
            mapped_price_line << [date, open * coeff, close * coeff]
          else
            if (bm_value = benchmark_by_date[date])
              coeff = bm_value / close
              mapped_price_line << [date, open * coeff, close * coeff]
            end
          end
        end

        res << [name, mapped_price_line]
      end
    end

    [benchmark, res]
  end

  def custom_index_params
    {"review_period"=>"quarterly", "filter_listing"=>["2"], "topcap_count"=>"50", "selection"=>"selection_momentum", "momentum_days"=>"365", "weighing"=>"equal", "index_name"=>"Мой ёлки", "commit"=>"Произвести расчёт"}

    filters = []

    if params[:filter_listing].present?
      filters << [IndexCalculator::FILTERS_LL, params[:filter_listing].map(&:to_i)]
    end

    if params[:filter_sector].present?
      filters << [IndexCalculator::FILTERS_SECTOR, params[:filter_sector].map(&:to_i)]
    end

    if params[:filter_tickers].present?
      filters << [IndexCalculator::FILTERS_TICKERS, params[:filter_tickers]]
    end

    selection = case params[:selection]
    when "selection_topcap"
      [
        IndexCalculator::SELECTION_MARKET_CAP,
        { IndexCalculator::SELECTION_TOP => params[:topcap_count].to_i }
      ]
    when "selection_momentum"
      [
        IndexCalculator::SELECTION_MOMENTUM,
        {
          IndexCalculator::SELECTION_PERIOD => params[:momentum_days].to_i, IndexCalculator::SELECTION_BENCHMARK => "IMOEX"
        }
      ]
    else
      raise "Unknown selection: `#{params[:selection]}`"
    end

    {
      name: params[:index_name],
      user: current_user,
      settings: {
        IndexCalculator::REVIEW_PERIOD => params[:review_period],
        IndexCalculator::FILTERS => filters,
        IndexCalculator::SELECTION => selection,
        IndexCalculator::WEIGHING => params[:weighing]
      }
    }
  end
end
