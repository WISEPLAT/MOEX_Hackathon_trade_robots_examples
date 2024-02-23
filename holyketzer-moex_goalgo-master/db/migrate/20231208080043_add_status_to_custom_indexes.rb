class AddStatusToCustomIndexes < ActiveRecord::Migration[7.1]
  def change
    add_column :custom_indices, :status, :string, null: false, default: "new"
    add_column :custom_indices, :progress, :integer, null: false, default: 0
    add_column :custom_indices, :error, :string
  end
end
