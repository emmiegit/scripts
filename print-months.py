#!/usr/bin/env python3

import calendar

if __name__ == "__main__":
    for num in range(1, 13):
        month = calendar.month_name[num]
        print(f"{num:02} - {month}")
