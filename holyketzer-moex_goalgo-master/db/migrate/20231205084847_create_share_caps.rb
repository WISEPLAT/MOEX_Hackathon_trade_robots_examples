class CreateShareCaps < ActiveRecord::Migration[7.1]
  def change
    create_table :share_caps do |t|
      t.references :share, null: false
      t.string :secid, null: false
      t.date :date, null: false
      t.bigint :cap, null: false

      t.timestamps

      t.index [:share_id, :date], unique: true
      t.index [:secid]
    end
  end
end
