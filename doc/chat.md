# General Chat API

>  - Unified chat API interface supporting all text generation models
- Select different AI models via the model parameter
- Compatible with OpenAI Chat Completions API format 

<RequestExample>
  ```bash cURL theme={null}
  curl --request POST \
    --url https://api.apimart.ai/v1/chat/completions \
    --header 'Authorization: Bearer <token>' \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "gpt-4o", # Can be replaced with any supported model ID
      "messages": [
        {
          "role": "system",
          "content": "You are a professional AI assistant."
        },
        {
          "role": "user",
          "content": "Tell me about the history of artificial intelligence."
        }
      ]
    }'
  ```

  ```python Python theme={null}
  import requests

  url = "https://api.apimart.ai/v1/chat/completions"

  payload = {
      "model": "gpt-4o",  # Can be replaced with any supported model ID
      "messages": [
          {
              "role": "system",
              "content": "You are a professional AI assistant."
          },
          {
              "role": "user",
              "content": "Tell me about the history of artificial intelligence."
          }
      ]
  }

  headers = {
      "Authorization": "Bearer <token>",
      "Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  print(response.json())
  ```

  ```javascript JavaScript theme={null}
  const url = "https://api.apimart.ai/v1/chat/completions";

  const payload = {
    model: "gpt-4o",  // Can be replaced with any supported model ID
    messages: [
      {
        role: "system",
        content: "You are a professional AI assistant."
      },
      {
        role: "user",
        content: "Tell me about the history of artificial intelligence."
      }
    ]
  };

  const headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
  };

  fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  ```

  ```go Go theme={null}
  package main

  import (
      "bytes"
      "encoding/json"
      "fmt"
      "io/ioutil"
      "net/http"
  )

  func main() {
      url := "https://api.apimart.ai/v1/chat/completions"

      payload := map[string]interface{}{
          "model": "gpt-4o",  // Can be replaced with any supported model ID
          "messages": []map[string]string{
              {
                  "role":    "system",
                  "content": "You are a professional AI assistant.",
              },
              {
                  "role":    "user",
                  "content": "Tell me about the history of artificial intelligence.",
              },
          },
      }

      jsonData, _ := json.Marshal(payload)

      req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
      req.Header.Set("Authorization", "Bearer <token>")
      req.Header.Set("Content-Type", "application/json")

      client := &http.Client{}
      resp, err := client.Do(req)
      if err != nil {
          panic(err)
      }
      defer resp.Body.Close()

      body, _ := ioutil.ReadAll(resp.Body)
      fmt.Println(string(body))
  }
  ```

  ```java Java theme={null}
  import java.net.http.HttpClient;
  import java.net.http.HttpRequest;
  import java.net.http.HttpResponse;
  import java.net.URI;

  public class Main {
      public static void main(String[] args) throws Exception {
          String url = "https://api.apimart.ai/v1/chat/completions";

          // Can be replaced with any supported model ID
          String payload = """
          {
            "model": "gpt-4o",
            "messages": [
              {
                "role": "system",
                "content": "You are a professional AI assistant."
              },
              {
                "role": "user",
                "content": "Tell me about the history of artificial intelligence."
              }
            ]
          }
          """;

          HttpClient client = HttpClient.newHttpClient();
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create(url))
              .header("Authorization", "Bearer <token>")
              .header("Content-Type", "application/json")
              .POST(HttpRequest.BodyPublishers.ofString(payload))
              .build();

          HttpResponse<String> response = client.send(request,
              HttpResponse.BodyHandlers.ofString());

          System.out.println(response.body());
      }
  }
  ```

  ```php PHP theme={null}
  <?php

  $url = "https://api.apimart.ai/v1/chat/completions";

  // Can be replaced with any supported model ID
  $payload = [
      "model" => "gpt-4o",
      "messages" => [
          [
              "role" => "system",
              "content" => "You are a professional AI assistant."
          ],
          [
              "role" => "user",
              "content" => "Tell me about the history of artificial intelligence."
          ]
      ]
  ];

  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_POST, true);
  curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
  curl_setopt($ch, CURLOPT_HTTPHEADER, [
      "Authorization: Bearer <token>",
      "Content-Type: application/json"
  ]);

  $response = curl_exec($ch);
  curl_close($ch);

  echo $response;
  ?>
  ```

  ```ruby Ruby theme={null}
  require 'net/http'
  require 'json'
  require 'uri'

  url = URI("https://api.apimart.ai/v1/chat/completions")

  # Can be replaced with any supported model ID
  payload = {
    model: "gpt-4o",
    messages: [
      {
        role: "system",
        content: "You are a professional AI assistant."
      },
      {
        role: "user",
        content: "Tell me about the history of artificial intelligence."
      }
    ]
  }

  http = Net::HTTP.new(url.host, url.port)
  http.use_ssl = true

  request = Net::HTTP::Post.new(url)
  request["Authorization"] = "Bearer <token>"
  request["Content-Type"] = "application/json"
  request.body = payload.to_json

  response = http.request(request)
  puts response.body
  ```

  ```swift Swift theme={null}
  import Foundation

  let url = URL(string: "https://api.apimart.ai/v1/chat/completions")!

  let payload: [String: Any] = [
      "model": "gpt-4o",  // Can be replaced with any supported model ID
      "messages": [
          [
              "role": "system",
              "content": "You are a professional AI assistant."
          ],
          [
              "role": "user",
              "content": "Tell me about the history of artificial intelligence."
          ]
      ]
  ]

  var request = URLRequest(url: url)
  request.httpMethod = "POST"
  request.setValue("Bearer <token>", forHTTPHeaderField: "Authorization")
  request.setValue("application/json", forHTTPHeaderField: "Content-Type")
  request.httpBody = try? JSONSerialization.data(withJSONObject: payload)

  let task = URLSession.shared.dataTask(with: request) { data, response, error in
      if let error = error {
          print("Error: \(error)")
          return
      }
      
      if let data = data, let responseString = String(data: data, encoding: .utf8) {
          print(responseString)
      }
  }

  task.resume()
  ```

  ```csharp C# theme={null}
  using System;
  using System.Net.Http;
  using System.Text;
  using System.Threading.Tasks;

  class Program
  {
      static async Task Main(string[] args)
      {
          var url = "https://api.apimart.ai/v1/chat/completions";

          // Can be replaced with any supported model ID
          var payload = @"{
              ""model"": ""gpt-4o"",
              ""messages"": [
                  {
                      ""role"": ""system"",
                      ""content"": ""You are a professional AI assistant.""
                  },
                  {
                      ""role"": ""user"",
                      ""content"": ""Tell me about the history of artificial intelligence.""
                  }
              ]
          }";

          using var client = new HttpClient();
          client.DefaultRequestHeaders.Add("Authorization", "Bearer <token>");

          var content = new StringContent(payload, Encoding.UTF8, "application/json");
          var response = await client.PostAsync(url, content);
          var result = await response.Content.ReadAsStringAsync();

          Console.WriteLine(result);
      }
  }
  ```

  ```c C theme={null}
  #include <stdio.h>
  #include <curl/curl.h>

  int main(void) {
      CURL *curl;
      CURLcode res;

      curl_global_init(CURL_GLOBAL_DEFAULT);
      curl = curl_easy_init();

      if(curl) {
          const char *url = "https://api.apimart.ai/v1/chat/completions";
          // Can be replaced with any supported model ID
          const char *payload = "{"
              "\"model\":\"gpt-4o\","
              "\"messages\":[{\"role\":\"system\",\"content\":\"You are a professional AI assistant.\"},{\"role\":\"user\",\"content\":\"Tell me about the history of artificial intelligence.\"}]"
          "}";

          struct curl_slist *headers = NULL;
          headers = curl_slist_append(headers, "Authorization: Bearer <token>");
          headers = curl_slist_append(headers, "Content-Type: application/json");

          curl_easy_setopt(curl, CURLOPT_URL, url);
          curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload);
          curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

          res = curl_easy_perform(curl);

          if(res != CURLE_OK) {
              fprintf(stderr, "curl_easy_perform() failed: %s\n",
                      curl_easy_strerror(res));
          }

          curl_slist_free_all(headers);
          curl_easy_cleanup(curl);
      }

      curl_global_cleanup();
      return 0;
  }
  ```

  ```objectivec Objective-C theme={null}
  #import <Foundation/Foundation.h>

  int main(int argc, const char * argv[]) {
      @autoreleasepool {
          NSURL *url = [NSURL URLWithString:@"https://api.apimart.ai/v1/chat/completions"];
          
          NSDictionary *payload = @{
              @"model": @"gpt-4o",  // Can be replaced with any supported model ID
              @"messages": @[
                  @{
                      @"role": @"system",
                      @"content": @"You are a professional AI assistant."
                  },
                  @{
                      @"role": @"user",
                      @"content": @"Tell me about the history of artificial intelligence."
                  }
              ]
          };
          
          NSError *error;
          NSData *jsonData = [NSJSONSerialization dataWithJSONObject:payload
                                                            options:0
                                                              error:&error];
          
          NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
          [request setHTTPMethod:@"POST"];
          [request setValue:@"Bearer <token>" forHTTPHeaderField:@"Authorization"];
          [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
          [request setHTTPBody:jsonData];
          
          NSURLSessionDataTask *task = [[NSURLSession sharedSession] 
              dataTaskWithRequest:request
              completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                  if (error) {
                      NSLog(@"Error: %@", error);
                      return;
                  }
                  NSString *result = [[NSString alloc] initWithData:data 
                                                          encoding:NSUTF8StringEncoding];
                  NSLog(@"%@", result);
              }];
          
          [task resume];
          [[NSRunLoop mainRunLoop] run];
      }
      return 0;
  }
  ```

  ```ocaml OCaml theme={null}
  (* Requires cohttp and yojson libraries *)
  open Lwt
  open Cohttp
  open Cohttp_lwt_unix

  let url = "https://api.apimart.ai/v1/chat/completions"

  (* Can be replaced with any supported model ID *)
  let payload = {|{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a professional AI assistant."
      },
      {
        "role": "user",
        "content": "Tell me about the history of artificial intelligence."
      }
    ]
  }|}

  let () =
    let headers = Header.init ()
      |> fun h -> Header.add h "Authorization" "Bearer <token>"
      |> fun h -> Header.add h "Content-Type" "application/json"
    in
    let body = Cohttp_lwt.Body.of_string payload in
    
    let response = Client.post ~headers ~body (Uri.of_string url) >>= fun (resp, body) ->
      body |> Cohttp_lwt.Body.to_string >|= fun body_str ->
      print_endline body_str
    in
    Lwt_main.run response
  ```

  ```dart Dart theme={null}
  import 'dart:convert';
  import 'package:http/http.dart' as http;

  void main() async {
    final url = Uri.parse('https://api.apimart.ai/v1/chat/completions');
    
    // Can be replaced with any supported model ID
    final payload = {
      'model': 'gpt-4o',
      'messages': [
        {
          'role': 'system',
          'content': 'You are a professional AI assistant.'
        },
        {
          'role': 'user',
          'content': 'Tell me about the history of artificial intelligence.'
        }
      ]
    };
    
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer <token>',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(payload),
    );
    
    print(response.body);
  }
  ```

  ```r R theme={null}
  library(httr)
  library(jsonlite)

  url <- "https://api.apimart.ai/v1/chat/completions"

  # Can be replaced with any supported model ID
  payload <- list(
    model = "gpt-4o",
    messages = list(
      list(
        role = "system",
        content = "You are a professional AI assistant."
      ),
      list(
        role = "user",
        content = "Tell me about the history of artificial intelligence."
      )
    )
  )

  response <- POST(
    url,
    add_headers(
      Authorization = "Bearer <token>",
      `Content-Type` = "application/json"
    ),
    body = toJSON(payload, auto_unbox = TRUE),
    encode = "raw"
  )

  cat(content(response, "text"))
  ```
</RequestExample>

<ResponseExample>
  ```json 200 theme={null}
  {
    "code": 200,
    "data": {
      "id": "chatcmpl-9876543210",
      "object": "chat.completion",
      "created": 1677652288,
      "model": "gpt-4o",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "The history of artificial intelligence (AI) dates back to the 1950s...\n\n1. **Early Period (1950s-1960s)**: The proposal of the Turing Test marked the beginning of AI research...\n\n2. **Expert Systems Era (1970s-1980s)**: Rule-based systems began to be applied in medical diagnosis, financial analysis, and other fields...\n\n3. **Rise of Machine Learning (1990s-2000s)**: Statistical learning methods gradually became mainstream...\n\n4. **Deep Learning Revolution (2010s-Present)**: Breakthroughs in neural network technology brought explosive growth to AI..."
          },
          "finish_reason": "stop"
        }
      ],
      "usage": {
        "prompt_tokens": 28,
        "completion_tokens": 320,
        "total_tokens": 348
      }
    }
  }
  ```

  ```json 400 theme={null}
  {
    "error": {
      "code": 400,
      "message": "Invalid request parameters",
      "type": "invalid_request_error"
    }
  }
  ```

  ```json 401 theme={null}
  {
    "error": {
      "code": 401,
      "message": "Authentication failed, please check your API key",
      "type": "authentication_error"
    }
  }
  ```

  ```json 402 theme={null}
  {
    "error": {
      "code": 402,
      "message": "Insufficient account balance, please recharge",
      "type": "payment_required"
    }
  }
  ```

  ```json 403 theme={null}
  {
    "error": {
      "code": 403,
      "message": "Access forbidden, you don't have permission to access this resource",
      "type": "permission_error"
    }
  }
  ```

  ```json 429 theme={null}
  {
    "error": {
      "code": 429,
      "message": "Too many requests, please try again later",
      "type": "rate_limit_error"
    }
  }
  ```

  ```json 500 theme={null}
  {
    "error": {
      "code": 500,
      "message": "Internal server error, please try again later",
      "type": "server_error"
    }
  }
  ```

  ```json 502 theme={null}
  {
    "error": {
      "code": 502,
      "message": "Bad gateway, service temporarily unavailable",
      "type": "bad_gateway"
    }
  }
  ```
</ResponseExample>

## Authorizations

<ParamField header="Authorization" type="string" required>
  All API endpoints require Bearer Token authentication

  Get your API Key:

  Visit the [API Key Management Page](https://api.apimart.ai/console/token) to get your API Key

  Add it to the request header:

  ```
  Authorization: Bearer YOUR_API_KEY
  ```
</ParamField>

## Body

<ParamField body="model" type="string" required>
  Model name

  Supported models include:

  * **OpenAI**: `gpt-5`, `gpt-5-chat-latest`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-pro`
  * **Anthropic**: `claude-sonnet-4-5-20250929`, `claude-opus-4-1-20250805`, `claude-haiku-4-5-20251001`, `claude-opus-4-1-20250805-thinking`, `claude-sonnet-4-5-20250929-thinking`
  * **Google**: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-pro-thinking`, `gemini-2.5-flash-lite`
  * **DeepSeek**: `deepseek-v3.1-250821`, `deepseek-v3.1-think-250821`, `deepseek-v3-0324`
  * **Doubao**: `doubao-seed-1-6-251015`, `doubao-seed-1-6-flash-250828`, `doubao-seed-1-6-thinking-250715`
  * More models being added continuously...
</ParamField>

<ParamField body="messages" type="array" required>
  List of conversation messages

  Each message contains:

  * `role`: Role type (`system`, `user`, `assistant`)
  * `content`: Message content (string or multimodal content array)
</ParamField>

<ParamField body="temperature" type="number">
  Controls output randomness, range 0-2

  * Lower values (e.g., 0.2) make output more deterministic
  * Higher values (e.g., 1.8) make output more random

  Default: 1.0
</ParamField>

<ParamField body="max_tokens" type="integer">
  Maximum number of tokens to generate

  Different models have different maximum limits, please refer to specific model documentation
</ParamField>

<ParamField body="stream" type="boolean">
  Whether to use streaming output

  * `true`: Streaming response (SSE format)
  * `false`: Complete response at once

  Default: false
</ParamField>

<ParamField body="top_p" type="number">
  Nucleus sampling parameter, range 0-1

  Controls diversity of generated text, recommend using either this or temperature

  Default: 1.0
</ParamField>

<ParamField body="frequency_penalty" type="number">
  Frequency penalty, range -2.0 to 2.0

  Positive values reduce the likelihood of repeating the same words

  Default: 0
</ParamField>

<ParamField body="presence_penalty" type="number">
  Presence penalty, range -2.0 to 2.0

  Positive values increase the likelihood of talking about new topics

  Default: 0
</ParamField>

<ParamField body="stop" type="string or array">
  Stop sequences

  Up to 4 sequences where generation will stop when encountered
</ParamField>

<ParamField body="n" type="integer">
  Number of completions to generate

  Default: 1
</ParamField>

## Response

<ResponseField name="id" type="string">
  Unique identifier for the response
</ResponseField>

<ResponseField name="object" type="string">
  Object type, fixed as `chat.completion`
</ResponseField>

<ResponseField name="created" type="integer">
  Creation timestamp
</ResponseField>

<ResponseField name="model" type="string">
  The actual model name used
</ResponseField>

<ResponseField name="choices" type="array">
  List of generated responses

  <Expandable title="Properties">
    <ResponseField name="index" type="integer">
      Choice index
    </ResponseField>

    <ResponseField name="message" type="object">
      Message content

      <Expandable title="Properties">
        <ResponseField name="role" type="string">
          Role type (assistant)
        </ResponseField>

        <ResponseField name="content" type="string">
          Generated text content
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="finish_reason" type="string">
      Reason for completion

      Possible values:

      * `stop` - Natural completion
      * `length` - Maximum length reached
      * `content_filter` - Content filtered
      * `function_call` - Function call
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="usage" type="object">
  Token usage statistics

  <Expandable title="Properties">
    <ResponseField name="prompt_tokens" type="integer">
      Number of tokens in the input messages
    </ResponseField>

    <ResponseField name="completion_tokens" type="integer">
      Number of tokens in the generated content
    </ResponseField>

    <ResponseField name="total_tokens" type="integer">
      Total number of tokens
    </ResponseField>
  </Expandable>
</ResponseField>

## Supported Models

### OpenAI Series

* `gpt-5` - GPT-5 base model
* `gpt-5-chat-latest` - GPT-5 latest chat version
* `gpt-5-mini` - GPT-5 lightweight version, cost-effective
* `gpt-5-nano` - GPT-5 ultra-lightweight version
* `gpt-5-pro` - GPT-5 professional enhanced version

### Anthropic Series

* `claude-haiku-4-5-20251001` - Claude 4.5 fast response version
* `claude-sonnet-4-5-20250929` - Claude 4.5 balanced version
* `claude-opus-4-1-20250805` - Most powerful Claude 4.1 flagship model
* `claude-opus-4-1-20250805-thinking` - Claude 4.1 Opus deep thinking version
* `claude-sonnet-4-5-20250929-thinking` - Claude 4.5 Sonnet deep thinking version

### Google Series

* `gemini-2.5-flash` - Gemini 2.5 fast version
* `gemini-2.5-pro` - Gemini 2.5 professional version
* `gemini-2.5-flash-lite` - Gemini 2.5 ultra-lightweight version
* `gemini-2.5-pro-thinking` - Gemini 2.5 Pro deep thinking version

### DeepSeek Series

* `deepseek-v3.1-250821` - DeepSeek V3.1 base version
* `deepseek-v3.1-think-250821` - DeepSeek V3.1 thinking version
* `deepseek-v3-0324` - DeepSeek V3 standard version

### Doubao Series

* `doubao-seed-1-6-flash-250828` - Doubao Seed 1.6 fast version
* `doubao-seed-1-6-thinking-250715` - Doubao Seed 1.6 thinking version
* `doubao-seed-1-6-251015` - Doubao Seed 1.6 standard version

## Usage Examples

### Basic Conversation

```json  theme={null}
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

### System Prompt

```json  theme={null}
{
  "model": "claude-3-5-sonnet",
  "messages": [
    {"role": "system", "content": "You are a professional Python programming tutor"},
    {"role": "user", "content": "How to use list comprehensions?"}
  ]
}
```

### Multi-turn Conversation

```json  theme={null}
{
  "model": "gemini-2.0-flash",
  "messages": [
    {"role": "user", "content": "What is machine learning?"},
    {"role": "assistant", "content": "Machine learning is a branch of artificial intelligence..."},
    {"role": "user", "content": "Can you give me an example?"}
  ]
}
```

### Streaming Output

```json  theme={null}
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Write a poem about spring"}
  ],
  "stream": true
}
```
