class AddUserIdToCustomIndexes < ActiveRecord::Migration[7.1]
  def change
    add_reference :custom_indices, :user

    execute <<~SQL
      UPDATE custom_indices SET user_id = (SELECT id FROM users LIMIT 1)
    SQL

    change_column_null :custom_indices, :user_id, false
  end
end
