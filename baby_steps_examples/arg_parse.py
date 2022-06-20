#!/usr/bin/env python3

import argparse
from multiprocessing import reduction

parser = argparse.ArgumentParser(description='Calcular area de terreno')
parser.add_argument('-l','--largura', type=int, help='Largura do terreno')
parser.add_argument('-c','--comprimento', type=int, help='Comprimento do terreno')

args = parser.parse_args()

def calcula(largura, comprimento):
    area = largura * comprimento
    return area

if __name__ == '__main__':
    print('A area do terreno é %s m2' %calcula(args.largura,args.comprimento))


    