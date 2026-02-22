# Scraping System Documentation

## Overview
This project is a comprehensive scraping system designed to collect and process data from various sources. The system is organized in a modular way, with different components handling specific types of data collection and processing.

## Project Structure

### Main Components

1. **balapan.py**
   - Main entry point of the application
   - Orchestrates the scraping process
   - Handles scheduling and error recovery
   - Supports command-line arguments for configuration

2. **Parties Module**
   - **suppliers.py**: Handles supplier data collection and processing
   - **clients.py**: Manages client data collection and processing
   - Both components follow a similar pattern: load → clean → dump

3. **Products Module**
   - **products.py**: Manages product catalog data
   - Handles product information collection and updates

4. **Company Module**
   - **registers.py**: Manages register data
   - **stores.py**: Handles store information
   - **shifts.py**: Processes shift data
   - Each component follows the load → clean → dump pattern

5. **Documents Module**
   - **docs.py**: Main document processing system
   - Handles various document types:
     - Sales
     - Return Sales
     - Purchases
     - Return Purchases
     - Movements
     - Changes

## Data Flow

1. **Loading Phase**
   - Data is fetched from the source server
   - Raw data is stored temporarily

2. **Cleaning Phase**
   - Raw data is processed and formatted
   - Data validation and transformation
   - Removal of unnecessary information

3. **Dumping Phase**
   - Processed data is sent to the target system
   - Batch processing for efficiency
   - Error handling and logging

## Key Features

1. **Error Handling**
   - Comprehensive error catching and logging
   - Automatic retry mechanisms
   - Detailed error reporting

2. **Scheduling**
   - Configurable time intervals
   - Support for different server modes
   - Flexible date range processing

3. **Data Processing**
   - Batch processing capabilities
   - Data validation
   - Transformation and cleaning

4. **Logging**
   - Detailed operation logging
   - Error tracking
   - Performance monitoring

## Usage

### Basic Usage
```bash
python balapan.py [--skip_load]
```

### Command Line Arguments
- `--skip_load`: Skip the initial data loading phase

### Configuration
- Server modes and URLs are configured in `utils/config.py`
- Time intervals and processing parameters can be adjusted in the respective modules

## Data Types

1. **Suppliers**
   - Basic information
   - Creation dates
   - Cloudshop IDs

2. **Clients**
   - Client details
   - Validation status
   - Merged information

3. **Products**
   - Product catalog
   - Pricing information
   - Stock details

4. **Documents**
   - Sales records
   - Purchase orders
   - Movement records
   - Change logs

## Error Handling

The system implements a robust error handling mechanism:
- Automatic retry on failure
- Detailed error logging
- Graceful degradation
- Data integrity checks

## Performance Considerations

1. **Batch Processing**
   - Data is processed in batches for efficiency
   - Configurable batch sizes
   - Memory usage optimization

2. **Rate Limiting**
   - Built-in delays between requests
   - Configurable intervals
   - Server load management

## Maintenance

1. **Logging**
   - Operation logs
   - Error logs
   - Performance metrics

2. **Monitoring**
   - Process status tracking
   - Error rate monitoring
   - Performance metrics collection

## Security

1. **Data Protection**
   - Secure data transmission
   - API key management
   - Access control

2. **Error Handling**
   - Secure error reporting
   - No sensitive data exposure
   - Proper exception handling 