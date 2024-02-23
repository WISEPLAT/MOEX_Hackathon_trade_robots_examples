class CreateShareSectors < ActiveRecord::Migration[7.1]
  def change
    create_table :share_sectors do |t|
      t.string :name, null: false

      t.timestamps
      t.index :name, unique: true
    end

    add_column :shares, :share_sector_id, :bigint
  end
end
