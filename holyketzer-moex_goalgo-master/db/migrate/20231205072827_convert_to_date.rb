class ConvertToDate < ActiveRecord::Migration[7.1]
  def change
    add_column :share_macro_stats, :new_date, :date

    reversible do |dir|
      dir.up do
        execute <<-SQL
          UPDATE share_macro_stats SET new_date = to_date(date, 'YYYY-MM-DD');
        SQL
      end
    end

    remove_column :share_macro_stats, :date
    rename_column :share_macro_stats, :new_date, :date
    change_column_null :share_macro_stats, :date, false
  end
end
