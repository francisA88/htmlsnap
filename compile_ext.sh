# cd src/cpp;
# c++ -O3 -Wall -shared -std=c++17 -fPIC -Lultralight/bin -Iultralight/include -I. renderer.cpp -o librenderer.so -lAppCore -lUltralight -lUltralightCore -lWebCore -std=c++17 -lpthread -ldl;
# cd $OLDPWD;

#!/usr/bin/env sh

set -e

cd src/cpp

OS="$(uname -s 2>/dev/null || echo Windows)"

if echo "$OS" | grep -qi "mingw\|msys\|cygwin"; then
    echo "Building for Windows..."

    OUTPUT=renderer.dll

    g++ -O3 -Wall -shared -std=c++17 \
        -Iultralight/include \
        -I. \
        renderer.cpp \
        -o "..\\htmlsnap\\libs\\$OUTPUT" \
        -Lultralight/bin \
        -lAppCore \
        -lUltralight \
        -lUltralightCore \
        -lWebCore

elif echo "$OS" | grep -qi "linux"; then
    echo "Building for Linux..."

    OUTPUT=librenderer.so

    g++ -O3 -Wall -shared -std=c++17 -fPIC \
        -Iultralight/include \
        -I. \
        renderer.cpp \
        -o "../htmlsnap/libs/$OUTPUT" \
        -Lultralight/bin \
        -lAppCore \
        -lUltralight \
        -lUltralightCore \
        -lWebCore \
        -lpthread \
        -ldl

else
    echo "Unsupported platform: $OS"
    exit 1
fi

cd "$OLDPWD"
echo "Built $OUTPUT"
