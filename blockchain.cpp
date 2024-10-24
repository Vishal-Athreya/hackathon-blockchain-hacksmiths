#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <openssl/sha.h>
class Block {
public:
    int index;
    std::string previousHash;
    std::string timestamp;
    std::string data;
    std::string hash;

    Block(int idx, std::string prevHash, std::string data)
        : index(idx), previousHash(prevHash), data(data) {
        timestamp = getCurrentTime();
        hash = calculateHash();
    }

    std::string calculateHash() const {
        std::stringstream ss;
        ss << index << previousHash << timestamp << data;
        return sha256(ss.str());
    }

    static std::string sha256(const std::string& str) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(reinterpret_cast<const unsigned char*>(str.c_str()), str.size(), hash);
        std::stringstream ss;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
            ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
        }
        return ss.str();
    }

private:
    static std::string getCurrentTime() {
        auto now = std::time(nullptr);
        auto tm = *std::localtime(&now);
        std::ostringstream oss;
        oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }
};

class Blockchain {
public:
    Blockchain() {
        createBlock("Genesis Block", "0");
    }

    void createBlock(std::string data) {
        int index = chain.size();
        std::string previousHash = (index == 0) ? "0" : chain.back().hash;
        chain.emplace_back(index, previousHash, data);
    }

    void printChain() const {
        for (const auto& block : chain) {
            std::cout << "Block " << block.index << " [Hash: " << block.hash
                      << ", Prev Hash: " << block.previousHash
                      << ", Data: " << block.data
                      << ", Timestamp: " << block.timestamp << "]\n";
        }
    }

private:
    std::vector<Block> chain;
};

int main() {
    Blockchain myBlockchain;

    // Adding blocks to the blockchain
    myBlockchain.createBlock("First block data");
    myBlockchain.createBlock("Second block data");

    // Print the blockchain
    myBlockchain.printChain();

    return 0;
}
