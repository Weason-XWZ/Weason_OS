import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="uavcan program")
    parser.add_argument("-id", "--uavcanid", help="set serial uavcanid")
    args = parser.parse_args()


