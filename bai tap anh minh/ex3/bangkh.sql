CREATE TABLE kh (
    sv_id INT,
    gv_id INT,
    kh_name NVARCHAR(50),
    result INT,
    PRIMARY KEY (sv_id, gv_id),
    FOREIGN KEY (sv_id) REFERENCES sv(sv_id),
    FOREIGN KEY (gv_id) REFERENCES gv(gv_id)
);
