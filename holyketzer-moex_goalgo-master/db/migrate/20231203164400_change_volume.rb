class ChangeVolume < ActiveRecord::Migration[7.1]
  def change
    change_column :share_prices, :volume, :bigint
  end
end
