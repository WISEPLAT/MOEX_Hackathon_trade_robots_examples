class AddHistoryFromToShares < ActiveRecord::Migration[7.1]
  def change
    add_column :shares, :history_from, :date, null: true
    change_column_null :shares, :issue_date, true
    change_column_null :shares, :list_level, true
  end
end
