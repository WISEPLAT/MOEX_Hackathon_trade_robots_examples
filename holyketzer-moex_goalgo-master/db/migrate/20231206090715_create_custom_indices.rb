class CreateCustomIndices < ActiveRecord::Migration[7.1]
  def change
    create_table :custom_indices do |t|
      t.string :name, null: false
      t.json :settings, null: false

      t.timestamps

      t.index :name, unique: true
    end
  end
end
