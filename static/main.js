Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-awesome-dropzone",{
    url: "upload/",
    // maxFiles:2,
    // maxFilesize:2,
    acceptedFiles: '.txt',
    maxFiles: 100,
})