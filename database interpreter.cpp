#include <iostream>
#include <set>
#include <string>

bool isProductReal(const std::string& productId, const std::set<std::string>& realProducts) {
    return realProducts.find(productId) != realProducts.end();
}

int main() {
    // Set of real product IDs
    std::set<std::string> realProducts = {
        std::ifstream inputFile("database.txt"); // Open the file
    std::string line;

    // Check if the file opened successfully
    if (!inputFile) {
        std::cerr << "Unable to open file database.txt";
        return 1; // Return an error code
    }

    // Read the file line by line
    while (std::getline(inputFile, line)) {
        std::cout << "Read: " << line << std::endl; // Print each line
    }

    inputFile.close(); // Close the file
    return 0; // Successful execution
        
    };

    std::string inputProductId;

    std::cout << "Enter the product ID to check: ";
    std::cin >> inputProductId;

    if (isProductReal(inputProductId, realProducts)) {
        std::cout << "The product is REAL." << std::endl;
    } else {
        std::cout << "The product is FAKE." << std::endl;
    }

    return 0;
}