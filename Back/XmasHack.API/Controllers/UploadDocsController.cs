using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using XmasHack.API.Configuration;
using XmasHack.API.CRUD_API;
using XmasHack.API.CRUD_API.Models.Requests;

namespace XmasHack.API.Controllers
{

    [ApiController]
    [Route("[controller]")]
    public class UploadDocsController: Controller
    {
        private readonly AppSettings _appSettings;
        private readonly ICrudAPI _crudAPI;

        public UploadDocsController(IOptions<AppSettings> appSettings, ICrudAPI crudAPI)
        {
            _appSettings = appSettings.Value;
            _crudAPI = crudAPI;
        }

        [HttpPost]
        public async Task<IActionResult> UploadDocs([FromForm] List<IFormFile> files)
        {
           foreach(var file in files)
            {
                try
                {
                    string fileName = $"{Guid.NewGuid()}-{file.FileName}";
                    await SaveDocsToFolder(file, fileName);
                    await _crudAPI.SaveDocs(new SaveDocsRequest()
                    {
                        FileName = file.FileName,
                        FilePath = fileName
                    });
                }
                catch(Exception ex)
                {
                    return BadRequest($"Ошибка во время сохрвнения файла: {file.FileName}. {ex.Message}");
                }
               
            }
            return Ok("Документы успешно сохранены");

        }

        private  async Task SaveDocsToFolder(IFormFile file, string docsName)
        {
            string filePath = Path.Combine(_appSettings.DocumentPath, docsName);
            using (Stream fileStream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(fileStream);
            }
        }
    }
}
