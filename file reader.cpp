#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string filePath = "C:\Users\visha\OneDrive\Desktop\database.txt"; // Replace with the actual file path

    ifstream inputFile(filePath);

    if (!inputFile.is_open()) {
        cerr << "Error opening file: " << filePath << endl;
        return 1;
    }

    string line;
    while (getline(inputFile, line)) {
        cout << line << endl;
    }

    inputFile.close();

    return 0;
}