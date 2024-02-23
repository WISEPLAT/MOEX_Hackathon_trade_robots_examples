class CustomIndex < ApplicationRecord
  validates :name, presence: true
  validates :name, uniqueness: true
  validates :settings, presence: true

  belongs_to :user

  def __example_of_settings__
    # Model CustomIndex
    {
      review_period: "quarterly", # or "yearly" Формирование Базы расчета
      filters: [
        ["listing_level", [1]],
        ["tickers", ["SBER", "GAZP", "LKOH", "GMKN", "ROSN", "NVTK", "TATN", "SNGS", "VTBR", "SBERP"]],
        ["sector", "Energy"],
      ],
      selection: ["market_cap", {"top": 50}], # ["momentum", {"period": 365, "benchmark": "MOEX"}]
      weighing: "equal", # or "market_cap"
    }
  end
end
