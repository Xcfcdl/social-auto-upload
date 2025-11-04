# Get Task Status

>  - Query the execution status and result of an asynchronous task
- Real-time status updates and progress tracking
- Retrieve generation results when tasks are completed 

<RequestExample>
  ```bash cURL theme={null}
  curl --request GET \
    --url https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt \
    --header 'Authorization: Bearer <token>'
  ```

  ```python Python theme={null}
  import requests

  url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt"

  headers = {
      "Authorization": "Bearer <token>"
  }

  response = requests.get(url, headers=headers)

  print(response.json())
  ```

  ```javascript JavaScript theme={null}
  const url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt";

  const headers = {
    "Authorization": "Bearer <token>"
  };

  fetch(url, {
    method: "GET",
    headers: headers
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  ```

  ```go Go theme={null}
  package main

  import (
      "fmt"
      "io/ioutil"
      "net/http"
  )

  func main() {
      url := "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt"

      req, _ := http.NewRequest("GET", url, nil)
      req.Header.Set("Authorization", "Bearer <token>")

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
          String url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt";

          HttpClient client = HttpClient.newHttpClient();
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create(url))
              .header("Authorization", "Bearer <token>")
              .GET()
              .build();

          HttpResponse<String> response = client.send(request,
              HttpResponse.BodyHandlers.ofString());

          System.out.println(response.body());
      }
  }
  ```

  ```php PHP theme={null}
  <?php

  $url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt";

  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_HTTPHEADER, [
      "Authorization: Bearer <token>"
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

  url = URI("https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt")

  http = Net::HTTP.new(url.host, url.port)
  http.use_ssl = true

  request = Net::HTTP::Get.new(url)
  request["Authorization"] = "Bearer <token>"

  response = http.request(request)
  puts response.body
  ```

  ```swift Swift theme={null}
  import Foundation

  let url = URL(string: "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt")!

  var request = URLRequest(url: url)
  request.httpMethod = "GET"
  request.setValue("Bearer <token>", forHTTPHeaderField: "Authorization")

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
  using System.Threading.Tasks;

  class Program
  {
      static async Task Main(string[] args)
      {
          var url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt";

          using var client = new HttpClient();
          client.DefaultRequestHeaders.Add("Authorization", "Bearer <token>");

          var response = await client.GetAsync(url);
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
          const char *url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt";

          struct curl_slist *headers = NULL;
          headers = curl_slist_append(headers, "Authorization: Bearer <token>");

          curl_easy_setopt(curl, CURLOPT_URL, url);
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
          NSURL *url = [NSURL URLWithString:@"https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt"];
          
          NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
          [request setHTTPMethod:@"GET"];
          [request setValue:@"Bearer <token>" forHTTPHeaderField:@"Authorization"];
          
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

  let url = "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt"

  let () =
    let headers = Header.init ()
      |> fun h -> Header.add h "Authorization" "Bearer <token>"
    in
    
    let response = Client.get ~headers (Uri.of_string url) >>= fun (resp, body) ->
      body |> Cohttp_lwt.Body.to_string >|= fun body_str ->
      print_endline body_str
    in
    Lwt_main.run response
  ```

  ```dart Dart theme={null}
  import 'package:http/http.dart' as http;

  void main() async {
    final url = Uri.parse('https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt');
    
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer <token>',
      },
    );
    
    print(response.body);
  }
  ```

  ```r R theme={null}
  library(httr)

  url <- "https://api.apimart.ai/v1/tasks/task-unified-1757156493-imcg5zqt"

  response <- GET(
    url,
    add_headers(
      Authorization = "Bearer <token>"
    )
  )

  cat(content(response, "text"))
  ```
</RequestExample>

<ResponseExample>
  ```json 200 theme={null}
  {
    "code": 200,
    "data": {
      "id": "task-unified-1757156493-k9m2xpvw",
      "status": "completed",
      "progress": 100,
      "result": {
        "images": [
          {
            "url": "https://example.com/generated-image.png",
            "expires_at": 1757242893
          }
        ]
      },
      "created": 1757156493,
      "completed": 1757156593,
      "estimated_time": 100,
      "actual_time": 100
    }
  }
  ```

  ```json 400 theme={null}
  {
    "error": {
      "code": 400,
      "message": "Invalid task ID",
      "type": "invalid_request_error"
    }
  }
  ```

  ```json 401 theme={null}
  {
    "error": {
      "code": 401,
      "message": "Invalid authentication credentials",
      "type": "authentication_error"
    }
  }
  ```

  ```json 402 theme={null}
  {
    "error": {
      "code": 402,
      "message": "Insufficient balance. Please top up your account",
      "type": "payment_required"
    }
  }
  ```

  ```json 403 theme={null}
  {
    "error": {
      "code": 403,
      "message": "Access forbidden. You don't have permission to access this resource",
      "type": "permission_error"
    }
  }
  ```

  ```json 429 theme={null}
  {
    "error": {
      "code": 429,
      "message": "Rate limit exceeded. Please try again later",
      "type": "rate_limit_error"
    }
  }
  ```

  ```json 500 theme={null}
  {
    "error": {
      "code": 500,
      "message": "Internal server error. Please try again later",
      "type": "server_error"
    }
  }
  ```

  ```json 502 theme={null}
  {
    "error": {
      "code": 502,
      "message": "Bad gateway. The server is temporarily unavailable",
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

## Path parameters

<ParamField path="task_id" type="string" required>
  Task ID returned by the generation API
</ParamField>

## Response

<ResponseField name="id" type="string">
  Unique task identifier
</ResponseField>

<ResponseField name="status" type="string">
  Task status values:

  * `pending` - Queued for processing
  * `processing` - In progress
  * `completed` - Finished successfully
  * `failed` - Failed
  * `cancelled` - Cancelled by user
</ResponseField>

<ResponseField name="progress" type="integer">
  Task progress percentage (0–100)
</ResponseField>

<ResponseField name="result" type="object">
  Task result, returned only when status is `completed`

  <Expandable title="Properties">
    <ResponseField name="images" type="array">
      Array of generated image objects (for image generation tasks)
    </ResponseField>

    <ResponseField name="videos" type="array">
      Array of generated video objects (for video generation tasks)
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="created" type="integer">
  Task creation timestamp
</ResponseField>

<ResponseField name="completed" type="integer">
  Task completion timestamp (only present when completed)
</ResponseField>

<ResponseField name="estimated_time" type="integer">
  Estimated completion time in seconds
</ResponseField>

<ResponseField name="actual_time" type="integer">
  Actual completion time in seconds (only present when completed)
</ResponseField>

<ResponseField name="error" type="object">
  Error details (only present when status is `failed`)

  <Expandable title="Properties">
    <ResponseField name="code" type="integer">
      Error code
    </ResponseField>

    <ResponseField name="message" type="string">
      Error message
    </ResponseField>

    <ResponseField name="type" type="string">
      Error type
    </ResponseField>
  </Expandable>
</ResponseField>
