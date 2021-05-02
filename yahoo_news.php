<!DOCTYPE html>
<html lang="ko">
<head>
  <title>일본 뉴스 모음</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <style>
    /* Set height of the grid so .sidenav can be 100% (adjust if needed) */
    .row.content {height: 1500px}

    /* Set gray background color and 100% height */
    .sidenav {
      background-color: #f1f1f1;
      height: 100%;
    }

    /* Set black background color, white text and some padding */
    footer {
      background-color: #555;
      color: white;
      padding: 15px;
    }

    /* On small screens, set height to 'auto' for sidenav and grid */
    @media screen and (max-width: 767px) {
      .sidenav {
        height: auto;
        padding: 15px;
      }
      .row.content {height: auto;}
    }
  </style>
</head>
<body>

<div class="container-fluid">
  <div class="row content">
    <div class="col-sm-2 sidenav">
      <h4>メニュー</h4>
      <ul class="nav nav-pills nav-stacked">
        <li><a href="http://127.0.0.1/index.php">Naverのニュース</a></li>
        <li class="active"><a href="http://127.0.0.1/yahoo_news.php">Yahooのニュース</a></li>
        <li><a href="https://www.kr.emb-japan.go.jp/itprtop_ko/index.html">在大韓民国日本国大使館</a></li>
      </ul><br>
      <div class="input-group">
      </div>
    </div>

    <div class="col-sm-9">
  <h2>Yahooのニュース</h2>
  <table class="table table-striped">
    <thead>
      <tr>
        <th style="width: 10%">日付</th>
        <th>タイトル</th>
      </tr>
    </thead>
    <tbody>

        <?php
        $host = "127.0.0.1";
        $_id = "news";
        $_password = "password";
        $_db_name = "jpn_news";
        $today = date("Y-m-d");

        $con = mysqli_connect($host, $_id, $_password, $_db_name);

        mysqli_query($con, "set session character_set_connection=utf8;");
        mysqli_query($con, "set session character_set_results=utf8;");
        mysqli_query($con, "set session character_set_client=utf8;");

        $sql = "SELECT * FROM jpn_yahoo_news WHERE DATE(date)='{$today}.' ORDER BY date DESC";
        $result = mysqli_query($con, $sql);

        while($row = mysqli_fetch_array($result)){
                echo '<tr><td>' .$row['date'].'</td><td><a href="'.$row['url'].'">'.$row['title'].'</a></td></tr>';}

        ?>
    </tbody>
  </table>
</div>
</body>
</html>
