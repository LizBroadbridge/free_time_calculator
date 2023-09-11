require 'csv'
require 'time'
require 'set'

contents = CSV.read("free_time_calculations.csv")

free_time = contents.filter do |row|  # Only keep rows with 'Free' as a start of the Text.
  text = row[4]
  text[0..3] == "Free"  # Only look at first 5 chars of that colmn and check == 'Free'
end

categories = Set.new

free_time.each do |row|  # Figure out how many variations of 'Free' there are
  categories.add(row[4])
end

categories = categories.to_a  # convert to array

with_durations = free_time.each do |row|  # Add another column, the duration
  t0 = Time.parse(row[2])
  t1 = Time.parse(row[3])
  time_difference = t1 - t0
  seconds_duration = time_difference.to_i
  minutes_duration = seconds_duration / 60
  row << minutes_duration  # Append it to row, creating new column
end

b_week_free_time = {}  # Create dict

with_durations.each do |row|
  next unless row[0] == "B" || row[0] == "Both"
  day = row[1]  # Pull out relevant columns
  text = row[4]
  duration = row[5]

  unless b_week_free_time[day]  # Dict, first key is each day, each value for those is also a dict
    b_week_free_time[day] = {}  # Each key in second dict is the category of free time
  end

  if b_week_free_time[day][text]
    b_week_free_time[day][text] += duration  # For each day, creating a total by category
  else
    b_week_free_time[day][text] = duration
  end
end

b_week_free_time_tabular = []

b_week_free_time.each do |k,v|  # Go over each key and value in dict (key being day of week, value category total of that day)
  vals = categories.map do |category|
    v[category] || 0
  end
  b_week_free_time_tabular << [k] + vals  # Adding to array anther element for each day of the week, the element also an array and first element is the day of week and next elementes are duration total for each categry
end

a_week_free_time = {}

with_durations.each do |row|
  next unless row[0] == "A" || row[0] == "Both"
  day = row[1]
  text = row[4]
  duration = row[5]

  unless a_week_free_time[day]
    a_week_free_time[day] = {}
  end

  if a_week_free_time[day][text]
    a_week_free_time[day][text] += duration
  else
    a_week_free_time[day][text] = duration
  end
end

a_week_free_time_tabular = []

a_week_free_time.each do |k,v|
  vals = categories.map do |category|
    v[category] || 0
  end
  a_week_free_time_tabular << [k] + vals
end

two_week_free_time = {}

with_durations.each do |row|
  multiplier = row[0] == "Both" ? 2 : 1
  day = row[1]
  text = row[4]
  duration = row[5]

  unless two_week_free_time[day]
    two_week_free_time[day] = {}
  end

  if two_week_free_time[day][text]
    two_week_free_time[day][text] += duration * multiplier
  else
    two_week_free_time[day][text] = duration * multiplier
  end
end

two_week_free_time_tabular = []

two_week_free_time.each do |k,v|
  vals = categories.map do |category|
    v[category] || 0
  end
  two_week_free_time_tabular << [k] + vals
end

two_week_avg_free_time_tabular = []

two_week_free_time_tabular.each do |row|
  two_week_avg_free_time_tabular << [
    row[0]] + row[1..].map do |mins|
      mins / 2
    end
end

def print_table(table_data)
  # Calculate the maximum width for each column
  column_widths = table_data.transpose.map { |column| column.map(&:to_s).max_by(&:length).length }

  # Print the table header in Markdown format
  puts "| #{table_data[0].zip(column_widths).map { |cell, width| cell.to_s.ljust(width) }.join(' | ')} |"
  puts "| #{column_widths.map { |width| '-' * (width) }.join(' | ')} |"

  # Print the table data rows in Markdown format
  table_data[1..-1].each do |row|
    puts "| #{row.zip(column_widths).map { |cell, width| cell.to_s.ljust(width) }.join(' | ')} |"
  end
end

headers = ["Day"] + categories

def totals_row(data)
  # Initialize a totals array with zeros
  totals = [0] * (data.first.length - 1)

  # Iterate through the data and update the totals
  data.each do |row|
    row[1..].each_with_index do |value, index|
      totals[index] += value
    end
  end

  totals
end

a_week_table_data = [headers] + a_week_free_time_tabular
b_week_table_data = [headers] + b_week_free_time_tabular
two_week_table_data = [headers] + two_week_free_time_tabular
two_week_avg_table_data = [headers] + two_week_avg_free_time_tabular

a_week_table_data << ["Total"] + totals_row(a_week_free_time_tabular)
b_week_table_data << ["Total"] + totals_row(b_week_free_time_tabular)
two_week_table_data << ["Total"] + totals_row(two_week_free_time_tabular)
two_week_avg_table_data << ["Total"] + totals_row(two_week_avg_free_time_tabular)

def format_time(total_minutes)
  # Calculate the hours and remaining minutes
  hours = total_minutes / 60
  minutes = total_minutes % 60

  # Format the result as a string
  "#{hours}h#{minutes}"
end

a_week_table_data[1..].each do |row|
  row[1..].each_with_index do |value, index|
    row[index + 1] = format_time(value)
  end
end

b_week_table_data[1..].each do |row|
  row[1..].each_with_index do |value, index|
    row[index + 1] = format_time(value)
  end
end

two_week_table_data[1..].each do |row|
  row[1..].each_with_index do |value, index|
    row[index + 1] = format_time(value)
  end
end

two_week_avg_table_data[1..].each do |row|
  row[1..].each_with_index do |value, index|
    row[index + 1] = format_time(value)
  end
end

puts("A Week:")
print_table(a_week_table_data)

puts

puts("B Week:")
print_table(b_week_table_data)

puts

puts("Two Week:")
print_table(two_week_table_data)

puts

puts("Two Week Avg:")
print_table(two_week_avg_table_data)

