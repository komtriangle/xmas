using Microsoft.AspNetCore.Mvc;

namespace XmasHack.API.Controllers
{

    [ApiController]
    [Route("[controller]")]
    public class UploadDocsController: Controller
    {

        [HttpPost]
        public async Task<IActionResult> UploadDocs([FromForm] List<IFormFile> files)
        {
           foreach(var file in files)
            {
                string name = file.FileName;
                string extension = Path.GetExtension(file.FileName);
                //read the file
                using (var memoryStream = new MemoryStream())
                {
                    file.CopyTo(memoryStream);
                }
               
            }
            return Ok();

        }
    }
}
