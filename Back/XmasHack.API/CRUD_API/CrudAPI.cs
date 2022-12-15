using System.Text;
using Newtonsoft.Json;
using XmasHack.API.CRUD_API.Models.Requests;
using XmasHack.API.CRUD_API.Models.Responses;

namespace XmasHack.API.CRUD_API
{
    public class CrudAPI : ICrudAPI
    {
        private readonly IHttpClientFactory _httpClientFactory;

        public CrudAPI(IHttpClientFactory httpClientFactory)
		{
            _httpClientFactory = httpClientFactory;
		}
        public async Task<int> SaveDocs(SaveDocsRequest request)
        {
            return 5;
			using(var httpClient = _httpClientFactory.CreateClient())
			{
                var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

                using(var response = await httpClient.PostAsync("/save_doc", content))
                {
                   if(response.StatusCode != System.Net.HttpStatusCode.Created)
                    {
                        throw new Exception("Ошибка при запросе в Crud API");
					}
                    var createDocsResponse = JsonConvert.DeserializeObject<CreateDocsResponse>(await response.Content.ReadAsStringAsync());

                    if(createDocsResponse == null)
                    {
                        throw new Exception("Ошибка во время десереализации ответа");
                    }

                    return createDocsResponse.Id;
                }
            }
        }

        public async Task<DocsResponse[]> GetAllDocs()
		{
            using(var httpClient = _httpClientFactory.CreateClient())
            {
                using(var response = await httpClient.GetAsync("/get_all_docs", HttpCompletionOption.ResponseHeadersRead))
                {
                    if(response.StatusCode != System.Net.HttpStatusCode.Created)
                    {
                        throw new Exception("Ошибка при запросе в Crud API");
                    }
                    var docses = JsonConvert.DeserializeObject<DocsResponse[]>(await response.Content.ReadAsStringAsync());

                    if(docses == null)
					{
                        throw new Exception("Ошибка во время получения списка документов");
					}

                    return docses;
                }
            }
        }
    }
}
