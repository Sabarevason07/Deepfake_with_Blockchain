
```markdown
# Deepfake Detection with Blockchain

A powerful system combining deep learning-based deepfake detection with blockchain technology for tamper-proof verification.

## Overview

This project provides an end-to-end pipeline to:

- Analyze media (images/videos) using AI to detect manipulations.
- Record verification results on a blockchain for transparency and immutability.
- Allow users to confirm media authenticity using stored metadata.

---

## Features

- **Deepfake Detection**: Utilizes CNNs, Vision Transformers, or other deep learning models.
- **Blockchain Logging**: Stores results such as file hash, detection verdict, verifier identity, and timestamp in a secure and immutable ledger.
- **Verification Tool**: Enables retrieving and validating past detection records using file hashes.
- **Web Interface**: Simple and intuitive UI for uploading, processing, and verifying media.
- **Scalable Architecture**: Designed to support large volumes of media and extendable for added features.

---

## Technology Stack

- **Deepfake Model**:
  - Python
  - OpenCV, NumPy, Pandas
  - TensorFlow or PyTorch

- **Blockchain**:
  - Ethereum, Hyperledger Fabric, or Polygon
  - Smart contract development in Solidity (or equivalent)

- **Backend & APIs**:
  - Flask or Django for serving API endpoints
  - RESTful architecture

- **Frontend**:
  - HTML, CSS (e.g., Bootstrap)
  - JavaScript (for interactivity)

---

## Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Sabarevason07/Deepfake_with_Blockchain.git
   cd Deepfake_with_Blockchain
````

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Deploy the smart contract**

   * Use Ganache or connect to a public testnet.
   * Run `python blockchain/deploy.py` to deploy your smart contract.
   * Save contract address and credentials in `.env`.

5. **Run the application**

   ```bash
   python web/app.py
   ```

   Navigate to `http://127.0.0.1:5000` to access the UI.

---

## Usage Workflow

1. **Upload media** via the web interface.
2. **Deepfake detection** is executed by the AI model.
3. The **result** (real or fake), along with file hash and timestamp, is stored on blockchain.
4. Use file hash to **verify** authenticity later.

---

## Smart Contract Schema

| Field              | Description                                   |
| ------------------ | --------------------------------------------- |
| `string fileHash`  | SHA-256 or similar hash of the media file     |
| `bool isFake`      | Whether the media is identified as a deepfake |
| `uint256 time`     | Timestamp of verification                     |
| `address verifier` | Address that performed the verification       |

---

## Future Enhancements

* Real-time deepfake detection for video streams.
* IPFS integration for decentralized media storage.
* Mobile app for on-the-go verification.
* Reporting/support integration with law enforcement or fact-checking services.
* Support for more advanced verification metrics (confidence scores, model explainability).

---

## Contributing

Contributions are most welcome! To contribute:

1. Fork the repo
2. Create a feature branch (`branch-name`)
3. Commit your changes
4. Push to your fork
5. Open a pull request for review

---

## License

MIT License — see [LICENSE](LICENSE) for details.
