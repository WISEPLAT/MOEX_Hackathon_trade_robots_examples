class AddStatsToCustomIndex < ActiveRecord::Migration[7.1]
  def change
    add_column :custom_indices, :avg_mr, :float
    add_column :custom_indices, :avg_yr, :float
    add_column :custom_indices, :max_md, :float
    add_column :custom_indices, :max_yd, :float
    add_column :custom_indices, :rsd, :float
    add_column :custom_indices, :sharp, :float
  end
end
