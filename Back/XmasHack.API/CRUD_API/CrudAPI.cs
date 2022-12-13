using XmasHack.API.CRUD_API.Models.Requests;

namespace XmasHack.API.CRUD_API
{
    public class CrudAPI : ICrudAPI
    {
        public Task SaveDocs(SaveDocsRequest request)
        {
            return Task.CompletedTask;
        }
    }
}
