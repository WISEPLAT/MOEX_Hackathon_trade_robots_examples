class AddListedTillToShares < ActiveRecord::Migration[7.1]
  def change
    add_column :shares, :listed_till, :date
  end
end
