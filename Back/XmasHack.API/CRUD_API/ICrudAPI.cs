using XmasHack.API.CRUD_API.Models.Requests;

namespace XmasHack.API.CRUD_API
{
    public interface ICrudAPI
    {
        public Task SaveDocs(SaveDocsRequest request);
    }
}
