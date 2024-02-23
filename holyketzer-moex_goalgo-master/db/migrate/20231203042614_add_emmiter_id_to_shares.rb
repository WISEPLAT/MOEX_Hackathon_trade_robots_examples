class AddEmmiterIdToShares < ActiveRecord::Migration[7.1]
  def change
    add_column :shares, :emmiter_id, :integer, null: true
    add_index :shares, :isin
  end
end
