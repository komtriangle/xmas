using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using XmasHack.API.Configuration;
using XmasHack.API.CRUD_API;
using XmasHack.API.CRUD_API.Models.Requests;
using XmasHack.API.Models;
using XmasHack.API.RabbitMQ;
using XmasHack.API.RabbitMQ.Contracts;

namespace XmasHack.API.Controllers
{

    [ApiController]
    [Route("[controller]")]
    public class UploadDocsController: Controller
    {
        private readonly AppSettings _appSettings;
        private readonly ICrudAPI _crudAPI;
        private readonly RabbitMQDocsPublisher _rabbitMQDocsPublisher;

        public UploadDocsController(IOptions<AppSettings> appSettings, IOptions<RabbitMQConfig> rabbitMQConfig, ICrudAPI crudAPI)
        {
            _appSettings = appSettings.Value;
            _crudAPI = crudAPI;
            _rabbitMQDocsPublisher = new RabbitMQDocsPublisher(rabbitMQConfig.Value);
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
                    int docsId = await _crudAPI.SaveDocs(new SaveDocsRequest()
                    {
                        FileName = file.FileName,
                        FilePath = fileName
                    });

                    _rabbitMQDocsPublisher.Send(new DocsMessage()
                    {
                        Id = docsId
                    });
                }
                catch(Exception ex)
                {
                    return BadRequest($"Ошибка во время сохрвнения файла: {file.FileName}. {ex.Message}");
                }
               
            }
            return Ok("Документы успешно сохранены");

        }

        [HttpGet]
        [Route("GetAllFiles")]
        public async Task<IActionResult> GetAllFiles()
        {
            return Ok(new FileResponse[]
            {
                new FileResponse()
                {
                    FileName="TD-2435_ux.pdf",
                    FilePath="5cf413ba-2952-4d23-9378-4366ab6ea365-TD-2435_ux.pdf",
                    Type = "Type 1"
                },
                new FileResponse()
                {
                    FileName ="Семинар(занания).docx",
                    FilePath="9c4daeee-aa9e-4ed5-92d4-185060ad5618-Семинар(занания).docx",
                    Type = "Type 2"
                },
                new FileResponse()
                {
                    FileName ="vertopal.com_Untitled52.pdf",
                    FilePath="a6f7415c-bdb1-498f-b9fc-250dd32f71bf-vertopal.com_Untitled52.pdf",
                    Type ="Type 3"
                }
            });
        }

        private  async Task SaveDocsToFolder(IFormFile file, string docsName)
        {
            string filePath = Path.Combine(_appSettings.DocumentPath, docsName);
            Console.WriteLine(filePath);
            using (Stream fileStream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(fileStream);
            }
        }
    }
}
