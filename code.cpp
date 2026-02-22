#include <iostream>
#include <cmath>
using namespace std;

bool isPerfectSquare(int x) {
    if (x < 0) return false;
    int r = (int)(sqrt(x) + 0.5);
    return r * r == x;
}

bool isPowerOfTwo(int x) {
    return x > 0 && (x & (x - 1)) == 0;
}

int main() {
    int n;
    cin>> n;

    for (int a = 1; a <= n; a++) {
        for (int b = a + 1; b <= n; b++) {
            for (int c = b + 1; c <= n; c++) {
                int f = a * b + b * c + c * a;

                if (isPerfectSquare(f) || isPowerOfTwo(f)) {
                    cout << "(" << a << ", " << b << ", " << c << ") -> "
                            << f;

                    if (isPerfectSquare(f)) cout << " [square]";
                    if (isPowerOfTwo(f)) cout << " [power of 2]";

                    cout << "\n";
                }
            }
        }
    }

    return 0;
}
