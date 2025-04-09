from plagiarismchecker.algorithm import ConsineSim
from apiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Multiple API keys for rotation
API_KEYS = [
    'AIzaSyAoEYif8sqEYvj1P6vYLw6CGMrQbDMmaq8',
    'AIzaSyCUYy9AtdMUddiNA0gOcsGPQcE372ytyCw', 
    'AIzaSyAQYLRBBeDQNxADPQtUnApntz78-urWEZI',
    'AIzaSyCAeR7_6TTKzoJmSwmOuHZvKcVg_lhqvCc'
]
searchEngine_Id = '758ad3e78879f0e08'

def searchWeb(text, output, c, retry_count=0):
    text = text
    current_key = random.choice(API_KEYS)  # Rotate keys
    
    try:
        resource = build("customsearch", 'v1',
                        developerKey=current_key).cse()
        result = resource.list(q=text, cx=searchEngine_Id).execute()
        
        searchInfo = result['searchInformation']
        if int(searchInfo['totalResults']) > 0:
            maxSim = 0
            itemLink = ''
            numList = min(len(result['items']), 5)  # Limit to 5 results
            
            for i in range(0, numList):
                item = result['items'][i]
                content = item['snippet']
                simValue = ConsineSim.cosineSim(text, content)
                
                if simValue > maxSim:
                    maxSim = simValue
                    itemLink = item['link']
                
                if item['link'] in output:
                    itemLink = item['link']
                    break

            if itemLink in output:
                output[itemLink] += 1
                c[itemLink] = ((c[itemLink] * (output[itemLink]-1) + maxSim)/output[itemLink])
            else:
                output[itemLink] = 1
                c[itemLink] = maxSim
                
        return output, c, 0
        
    except HttpError as e:
        if e.resp.status == 429:  # Rate limit exceeded
            if retry_count < 3:  # Max 3 retries
                wait_time = (2 ** retry_count) + random.random()  # Exponential backoff
                logger.warning(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                return searchWeb(text, output, c, retry_count + 1)
            else:
                logger.error("Max retries exceeded for rate limiting")
                return output, c, 1
        else:
            logger.error(f"Google API error: {str(e)}")
            return output, c, 1
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return output, c, 1
