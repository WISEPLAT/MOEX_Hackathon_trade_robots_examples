class CreateShareSplits < ActiveRecord::Migration[7.1]
  def change
    create_table :share_splits do |t|
      t.references :share, null: false
      t.date :date
      t.integer :before
      t.integer :after

      t.index [:share_id, :date], unique: true
    end
  end
end
