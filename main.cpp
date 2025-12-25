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
jbits/
├── jbits           ← compiled binary
├── JBits.dat       ← PRIVATE KEY (wallet)
├── jbits_log.csv   ← spreadsheet log (everything)
└── README.md
std::ofstream("JBits.dat");
std::ofstream("jbits_log.csv");