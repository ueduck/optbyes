#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from byesopt.optbyes import OptByes


def main() -> None:
    s = {1: (2, 3, 4), 2: (1, 4, 3), 3: (2, 1, 4), 4: (2, 3, 1)}
    p = OptByes(s)
    p.solve()
    p.printSchedule()


if __name__ == "__main__":
    main()
