python3 init.py projects/
./up.sh
./scripts/test.sh
res=$?
./down.sh
exit $res