#include <iostream>
#include <roxlu/core/Log.h>
#include <roxlu/core/Utils.h>
#include <twitter/Twitter.h>
#include <jansson/Jansson.h>

// gets called when we receive new data
void twitter_filter_cb(HTTPConnection* c, HTTPConnectionEvent event, 
                               const char* data, size_t len, void* user) 
{
  if(event == HTTP_ON_STATUS) {
    RX_VERBOSE("HTTP status: %d", c->parser.status_code);
  }
  else if(event == HTTP_ON_BODY) {
    // parse the tweet.
    std::string str(data, data+len);
    Tweet tweet;
    tweet.parseJSON(str);
    tweet.print();
  }
}

int main() {
  
  Jansson config;
  if(!config.load("twitter.json", true)) {
    RX_ERROR("Cannot load the twitter.json file with the config tokens");
    ::exit(EXIT_FAILURE);
  }
  std::string access_token;
  std::string access_token_secret;
  std::string consumer_key;
  std::string consumer_secret;

  if(!config.getString("/access_token", access_token) 
     || !config.getString("/access_token_secret", access_token_secret)
     || !config.getString("/consumer_key", consumer_key)
     || !config.getString("/consumer_secret", consumer_secret))
    {
      RX_ERROR("Cannot find the correct values in the config file");
      ::exit(EXIT_FAILURE);
    }

  Twitter tw;
  bool r =  tw.setup(access_token, access_token_secret, consumer_key, consumer_secret);

  if(!r) {
    RX_ERROR("Cannot setup the twitter obj");
    ::exit(EXIT_FAILURE);
  }

  // Track 
  TwitterStatusesFilter tw_filter;
  tw_filter.track("love,openframeworks"); // comma separated list of keywords to track
  tw.apiStatusesFilter(tw_filter, twitter_filter_cb, NULL);
  
  while(true) {
    tw.update();
  }

  return 0;
};

