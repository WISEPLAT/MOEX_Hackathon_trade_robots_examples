class CreateShareMacroStats < ActiveRecord::Migration[7.1]
  def change
    create_table :share_macro_stats do |t|
      t.references :share, null: false
      t.string :secid, null: false
      t.string :date, null: false
      t.bigint :shares_count, null: false
      t.money :cap

      t.timestamps

      t.index [:secid, :date], unique: true
    end

    add_column :shares, :version, :integer, null: false, default: 0
  end
end
