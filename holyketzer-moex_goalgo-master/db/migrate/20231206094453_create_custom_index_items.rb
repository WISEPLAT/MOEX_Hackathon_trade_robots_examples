class CreateCustomIndexItems < ActiveRecord::Migration[7.1]
  def change
    create_table :custom_index_items do |t|
      t.references :custom_index, null: false
      t.references :share, null: false
      t.decimal :shares_count, precision: 24, scale: 8, null: false # absolute count of shares
      t.date :date, null: false
      t.decimal :weight, precision: 10, scale: 8, null: false # relative weight of the share in the index

      t.index [:custom_index_id, :date], name: "index_custom_index_items_on_custom_index_id_and_date"
    end

    add_column :custom_indices, :coeff_d, :decimal, precision: 16, scale: 4

    create_table :custom_index_prices do |t|
      t.references :custom_index, null: false
      t.date :date, null: false
      t.decimal :open, precision: 10, scale: 2, null: false
      t.decimal :close, precision: 10, scale: 2, null: false
      # t.decimal :low, precision: 10, scale: 2, null: false
      # t.decimal :high, precision: 10, scale: 2, null: false
      # t.bigint :volume, null: false
    end
  end
end
