if [[ $1 == "clean" ]]; then
	make clean -C pca10056/s140/armgcc/
fi

make -C pca10056/s140/armgcc/ -j && cd pca10056/s140/armgcc/ && ./go.sh
