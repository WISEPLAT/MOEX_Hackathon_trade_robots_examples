class ChangePrecisionShares < ActiveRecord::Migration[7.1]
  def change
    change_column :share_prices, :open, :decimal, precision: 16, scale: 8
    change_column :share_prices, :close, :decimal, precision: 16, scale: 8
    change_column :share_prices, :low, :decimal, precision: 16, scale: 8
    change_column :share_prices, :high, :decimal, precision: 16, scale: 8
    change_column :share_prices, :waprice, :decimal, precision: 16, scale: 8
  end
end
