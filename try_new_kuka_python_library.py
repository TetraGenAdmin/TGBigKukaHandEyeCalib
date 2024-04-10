from kuka import Kuka


kuka = Kuka('172.31.1.147', 54600)

kuka.call_subroutine(2)
# kuka.set_base([0,0,0,0,0,0])