std::string private_key;
std::ifstream in("JBits.dat");

if (in.good()) {
    getline(in, private_key);
} else {
    private_key = random256();
    std::ofstream out("JBits.dat");
    out << private_key << "\n";
    out.close();
}