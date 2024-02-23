class AddCapToShares < ActiveRecord::Migration[7.1]
  def change
    add_column :shares, :cap, :money, null: true
  end
end
