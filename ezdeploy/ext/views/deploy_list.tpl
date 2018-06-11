% rebase('base.tpl')
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="/">部署列表<span class="sr-only">(current)</span></a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li>
    <a href="https://online.jenkins.com/jenkins/">Jenkins部署</a>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<div class="container">
    <table class="table">
      <tr>
	<td>部署日期</td>
	<td>服务</td>
	<td>环境</td>
	<td>包路径</td>
	<td>部署组</td>
	<td>部署环境</td>
	<td>Changelog</td>
        <td>发布详情</td>
	<td>打包日期</td>
      </tr>
      %for ditem in dlist:
      <tr>
	<td>{{ditem['ddate']}}</td>
	<td>{{ditem['service']}}</td>
	<td>{{ditem['penv']}}</td>
	<td>{{ditem['purl']}}</td>
	<td>{{ditem['dservice']}}</td>
	<td>{{ditem['denv']}}</td>
	<td>{{ditem['changelog']}}</td>
        <td>{{ditem['comment']}}</td>
	<td>{{ditem['pdate']}}</td>
      </tr>
      %end
    </table>
</div>

