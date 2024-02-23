class ChangeCapType < ActiveRecord::Migration[7.1]
  def change
    remove_column :share_macro_stats, :cap
    add_column :share_macro_stats, :cap, :bigint
  end
end
