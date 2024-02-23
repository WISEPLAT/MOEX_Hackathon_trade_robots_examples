require 'rails_helper'

RSpec.describe IndexCalculator do
  describe '.build_index' do
    let(:settings) do
      {
        IndexCalculator::REVIEW_PERIOD => IndexCalculator::REVIEW_PERIOD_Q,
        IndexCalculator::FILTERS => [
          [IndexCalculator::FILTERS_LL, 1],
          [IndexCalculator::FILTERS_TICKERS, ["SBER", "GAZP", "LKOH", "GMKN", "ROSN", "NVTK", "TATN", "SNGS", "VTBR", "SBERP"]],
          [IndexCalculator::FILTERS_SECTOR, "Energy"]
        ],
        IndexCalculator::SELECTION => [IndexCalculator::SELECTION_MARKET_CAP, { top: 50 }],
        IndexCalculator::WEIGHING => "equal"
      }
    end

    it 'builds the index' do
      expect { described_class.build_index }.not_to raise_error
      # Add more expectations here to verify the behavior of the method
      settings = {
        "review_period" => "quarterly",
        "filters" => [
          ["listing_level", 1]
        ],
        "selection" => ["market_cap", { "top": 25 }],
        "weighing" => "market_cap",
      }
      ci = CustomIndex.new(name: "test", settings: settings)
      IndexCalculator.build_index(CustomIndex.find(1))

      settings_m = {
        "review_period" => "quarterly",
        "filters" => [
          ["listing_level", 1]
        ],
        "selection" => ["momentum", {"period": 365, "benchmark": "IMOEX"}],
        "weighing" => "market_cap",
      }
      ci_m = CustomIndex.create!(name: "test_momentum", settings: settings_m)
      IndexCalculator.build_index(CustomIndex.find(2))
    end
  end
end
