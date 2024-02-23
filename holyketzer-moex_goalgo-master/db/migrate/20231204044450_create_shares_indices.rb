class CreateSharesIndices < ActiveRecord::Migration[7.1]
  def change
    create_table :shares_indices do |t|
      t.string :secid, null: false
      t.string :name, null: false
      t.string :short_name, null: false
      t.string :currency, null: false

      t.timestamps

      t.index :secid, unique: true
    end
  end
end
